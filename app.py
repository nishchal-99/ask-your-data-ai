import streamlit as st
import sqlite3
from openai import OpenAI

# ---- Setup ----

import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_query(query):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()
    return columns, results


def generate_sql(user_input):
    prompt = f"""
    You are a senior data analyst writing SQL for SQLite.

    Table: sales_data

    Columns:
    order_id, order_date, region, category,
    sub_category, product_name, sales,
    quantity, profit

    Rules:
    - Return ONLY SQL
    - No markdown
    - Use correct SQLite syntax

    User question:
    {user_input}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


# ---- UI ----
st.set_page_config(page_title="Ask Your Data", layout="wide")

st.title("📊 Ask Your Data")

st.caption(
    "AI-powered analytics assistant that converts natural language questions into SQL and visual insights."
)
st.write("Ask questions in plain English and get insights instantly.")

st.markdown("### Try asking:")
st.write("- Top 5 products by sales")
st.write("- Sales by region")
st.write("- Monthly sales trend")
st.write("- Most profitable category")

# Input box
user_input = st.text_input("Ask a question:")

if st.button("Run Query") and user_input:

    sql_query = generate_sql(user_input)

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    try:
        columns, results = run_query(sql_query)

        st.subheader("Results")

        # Convert to dataframe
        import pandas as pd
        df = pd.DataFrame(results, columns=columns)

        st.dataframe(df)

        # Optional chart
        if len(df.columns) >= 2:
            st.subheader("Chart")
            st.bar_chart(df.set_index(df.columns[0]))

    except Exception as e:
        st.error(f"Error: {e}")