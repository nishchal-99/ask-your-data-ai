import os
import tempfile

import pandas as pd
import streamlit as st

def reset_query():
    st.session_state.generated_sql = ""
    st.session_state.risk_report = None
    st.session_state.user_question = ""

from db import (
    create_sqlite_db_from_dataframe,
    get_schema_description,
    run_query,
)
from sql_engine import analyze_sql_risk, generate_sql


st.set_page_config(page_title="Ask Your Data", layout="wide")

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

    except Exception as e:
        st.error(f"Error reading CSV: {e}")


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

        except Exception as e:
            st.error(f"Error generating SQL: {e}")


if st.session_state.generated_sql:
    st.markdown("## 3. Generated SQL")

    sql_query = st.session_state.generated_sql
    risk_report = st.session_state.risk_report

    st.code(sql_query, language="sql")

    if risk_report["risk"] == "safe":
        st.success(risk_report["message"])

        if st.button("Run Query"):
            try:
                columns, results = run_query(
                    query=sql_query,
                    db_path=st.session_state.db_path,
                )

                st.markdown("## 4. Results")

                if columns:
                    result_df = pd.DataFrame(results, columns=columns)
                    st.dataframe(result_df, use_container_width=True)

                    if len(result_df.columns) >= 2 and not result_df.empty:
                        st.markdown("### Chart")

                        try:
                            chart_df = result_df.set_index(result_df.columns[0])
                            st.bar_chart(chart_df)
                        except Exception:
                            st.info("Chart could not be generated for this result.")
                else:
                    st.info("Query executed successfully. No rows were returned.")

            except Exception as e:
                st.error(f"Error running query: {e}")

    else:
        st.warning(risk_report["message"])

        st.markdown("### Detected Risk Keywords")
        st.code(", ".join(risk_report["keywords"]), language="text")

        st.error(
            "This query may modify, create, replace, or delete data. "
            "Review the SQL carefully before running it."
        )

        confirm = st.checkbox("I understand the risk and want to run this query.")

        if confirm and st.button("Run Risky Query"):
            try:
                columns, results = run_query(
                    query=sql_query,
                    db_path=st.session_state.db_path,
                )

                st.markdown("## 4. Results")

                if columns:
                    result_df = pd.DataFrame(results, columns=columns)
                    st.dataframe(result_df, use_container_width=True)

                    if len(result_df.columns) >= 2 and not result_df.empty:
                        st.markdown("### Chart")

                        try:
                            chart_df = result_df.set_index(result_df.columns[0])
                            st.bar_chart(chart_df)
                        except Exception:
                            st.info("Chart could not be generated for this result.")
                else:
                    st.info("Query executed successfully. No rows were returned.")

            except Exception as e:
                st.error(f"Error running query: {e}")

else:
    st.info("Upload a CSV file to begin.")

st.divider()

if st.session_state.db_path:

    st.button(

        "Reset query",

        on_click=reset_query,

    )