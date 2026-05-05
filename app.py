import os
import tempfile

import pandas as pd
import streamlit as st

from ai.error_fixer import fix_sql
from ai.sql_generator import generate_sql
from database.db_loader import create_sqlite_db_from_dataframe
from database.schema_reader import get_schema_description
from database.query_executor import run_query
from safety.query_safety import analyze_sql_risk
from safety.dry_run import build_delete_dry_run_query
from ai.query_explainer import explain_sql

from history.query_history import (
    add_query_to_history,
    load_history,
    toggle_favorite,
    clear_history,
)

from export.export_utils import dataframe_to_csv_bytes, sql_to_text_bytes

st.set_page_config(page_title="Ask Your Data", layout="wide")


def execute_and_display_query(
    sql_query,
    db_path,
    user_question=None,
    schema_description=None,
    table_name=None,
    allow_auto_fix=True,
):
    try:
        columns, results = run_query(
            query=sql_query,
            db_path=db_path,
        )

        st.markdown("## 4. Results")

        if columns:
            result_df = pd.DataFrame(results, columns=columns)
            st.dataframe(result_df, use_container_width=True)

            csv = dataframe_to_csv_bytes(result_df)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv",
            )

            if len(result_df.columns) >= 2 and not result_df.empty:
                st.markdown("### Chart")

                try:
                    chart_df = result_df.set_index(result_df.columns[0])
                    st.bar_chart(chart_df)
                except Exception:
                    st.info("Chart could not be generated for this result.")

            return result_df

        st.info("Query executed successfully. No rows were returned.")
        return None

    except Exception as error:
        st.error(f"SQL execution failed: {error}")

        if allow_auto_fix and user_question and schema_description and table_name:
            st.subheader("AI Auto-Fix Suggestion")

            fixed_sql = fix_sql(
                user_question=user_question,
                failed_sql=sql_query,
                error_message=str(error),
                schema_description=schema_description,
                table_name=table_name,
            )

            st.code(fixed_sql, language="sql")

            if st.button("Run fixed SQL"):
                return execute_and_display_query(
                    sql_query=fixed_sql,
                    db_path=db_path,
                    user_question=user_question,
                    schema_description=schema_description,
                    table_name=table_name,
                    allow_auto_fix=False,
                )

        return None


def reset_query():
    st.session_state.generated_sql = ""
    st.session_state.risk_report = None
    st.session_state.user_question = ""


st.title("Ask Your Data")
st.caption(
    "Upload your CSV, ask questions in English, and get SQL-powered answers."
)

st.markdown("## 1. Upload your CSV")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])


if "db_path" not in st.session_state:
    st.session_state.db_path = None

if "table_name" not in st.session_state:
    st.session_state.table_name = "uploaded_data"

if "schema_description" not in st.session_state:
    st.session_state.schema_description = ""

if "generated_sql" not in st.session_state:
    st.session_state.generated_sql = ""

if "risk_report" not in st.session_state:
    st.session_state.risk_report = None

if "user_question" not in st.session_state:
    st.session_state.user_question = ""


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("CSV uploaded successfully.")

        st.markdown("### Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        temp_dir = tempfile.gettempdir()
        db_path = os.path.join(temp_dir, "ask_your_data_uploaded.db")

        table_name = "uploaded_data"

        create_sqlite_db_from_dataframe(
            df=df,
            db_path=db_path,
            table_name=table_name,
        )

        schema_description = get_schema_description(
            df=df,
            table_name=table_name,
        )

        st.session_state.db_path = db_path
        st.session_state.table_name = table_name
        st.session_state.schema_description = schema_description

        st.markdown("### Detected Schema")
        st.code(schema_description, language="text")

    except Exception as error:
        st.error(f"Error reading CSV: {error}")


if st.session_state.db_path:
    st.markdown("## 2. Ask a question")

    st.write("Examples:")
    st.write("- Show top 5 rows")
    st.write("- Which category has the highest sales?")
    st.write("- Show total revenue by region")
    st.write("- Find average profit by product")
    st.write("- Delete rows where sales is empty")
    st.write("- Update missing region values to Unknown")

    user_input = st.text_input(
        "Ask a question about your uploaded CSV:",
        key="user_question",
    )

    if st.button("Generate SQL") and user_input:
        try:
            sql_query = generate_sql(
                user_input=user_input,
                schema_description=st.session_state.schema_description,
                table_name=st.session_state.table_name,
            )

            risk_report = analyze_sql_risk(sql_query)

            st.session_state.generated_sql = sql_query
            st.session_state.risk_report = risk_report

            add_query_to_history(
            question=user_input,
            sql_query=sql_query,
            risk_level=risk_report["risk"],
            )

        except Exception as error:
            st.error(f"Error generating SQL: {error}")


if st.session_state.generated_sql:
    st.markdown("## 3. Generated SQL")

    sql_query = st.session_state.generated_sql
    risk_report = st.session_state.risk_report

    st.code(sql_query, language="sql")

    st.download_button(
    label="Download SQL",
    data=sql_to_text_bytes(sql_query),
    file_name="generated_query.sql",
    mime="text/plain",
    )

    if st.button("Explain SQL"):
        explanation = explain_sql(
            sql_query=sql_query,
            user_question=st.session_state.user_question,
        )

        st.markdown("### SQL Explanation")
        st.write(explanation)

    if risk_report["risk"] == "safe":
        st.success(risk_report["message"])

        if st.button("Run Query"):
            execute_and_display_query(
                sql_query=sql_query,
                db_path=st.session_state.db_path,
                user_question=st.session_state.user_question,
                schema_description=st.session_state.schema_description,
                table_name=st.session_state.table_name,
            )

    else:
        if risk_report["risk"] == "medium":
            st.warning(risk_report["message"])
        else:
            st.error(risk_report["message"])

        st.markdown("### Detected Risk Keywords")
        st.code(", ".join(risk_report["keywords"]), language="text")

        dry_run_query = build_delete_dry_run_query(sql_query)

        if dry_run_query:
            st.markdown("### Dry Run Preview")
            st.code(dry_run_query, language="sql")

            try:
                dry_columns, dry_results = run_query(
                    query=dry_run_query,
                    db_path=st.session_state.db_path,
                )

                if dry_results:
                    affected_rows = dry_results[0][0]
                    st.warning(f"This query may affect {affected_rows} rows.")

            except Exception as error:
                st.warning(f"Could not generate dry-run preview: {error}")

        st.error(
            "This query may modify, create, replace, or delete data. "
            "Review the SQL carefully before running it."
        )

        confirm = st.checkbox("I understand the risk and want to run this query.")

        if confirm and st.button("Run Risky Query"):
            execute_and_display_query(
                sql_query=sql_query,
                db_path=st.session_state.db_path,
                user_question=st.session_state.user_question,
                schema_description=st.session_state.schema_description,
                table_name=st.session_state.table_name,
            )

else:
    st.info("Upload a CSV file to begin.")


st.markdown("## Query History")

history = load_history()

if history:
    if st.button("Clear History"):
        clear_history()
        st.rerun()

    for index, item in enumerate(history):
        favorite_label = "★ Favorite" if item.get("favorite") else "☆ Mark Favorite"

        with st.expander(f'{item["timestamp"]} — {item["question"]}'):
            st.write(f'Risk level: {item["risk_level"]}')
            st.code(item["sql_query"], language="sql")

            if st.button(favorite_label, key=f"favorite_{index}"):
                toggle_favorite(index)
                st.rerun()
else:
    st.info("No query history yet.")


st.divider()

if st.session_state.db_path:
    st.button(
        "Reset query",
        on_click=reset_query,
    )