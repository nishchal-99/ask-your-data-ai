import sqlite3
from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))def run_query(query):
    print("Executing:", query)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()
   
    print("Rows fetched:", len(results))
    conn.close()
    return results


def generate_sql(user_input):
    try:
        prompt = f"""
        You are a senior data analyst writing SQL for SQLite.

        Database schema:

        Table: sales_data

        Columns:
        order_id, order_date, region, category,
        sub_category, product_name, sales,
        quantity, profit

        Rules:
        - Use only these columns
        - Use correct SQLite syntax
        - Return ONLY raw SQL
        - Do NOT include markdown
        - If user asks "top" or "best", sort DESC
        - If user asks "least" or "worst", sort ASC
        - If user asks "trend", group by time

        User question:
        {user_input}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        sql = response.choices[0].message.content

        if sql is None:
            return ""

        sql = sql.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql

    except Exception as e:
        print("❌ Error generating SQL:", e)
        return ""


def fix_sql(user_input, bad_sql, error_message):
    prompt = f"""
    The following SQL query failed.

    User question: {user_input}

    Bad SQL:
    {bad_sql}

    Error:
    {error_message}

    Fix the SQL query.

    Return ONLY corrected SQL.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    fixed_sql = response.choices[0].message.content.strip()
    fixed_sql = fixed_sql.replace("```sql", "").replace("```", "").strip()

    return fixed_sql

chat_history = []

# ---- Run loop ----
while True:
    user_input = input("\nAsk a question (or type 'exit'): ")

    if user_input.lower() == "exit":
        break

    chat_history.append({"role": "user", "content": user_input})

    sql_query = generate_sql(user_input)

    print("\nGenerated SQL:")
    print(sql_query)

    # HANDLE EMPTY RESPONSE
    if not sql_query:
        print("⚠️ Failed to generate SQL. Try again.")
        continue

    # Safety check (ADD HERE)
    if any(keyword in sql_query.lower() for keyword in ["drop", "delete", "update", "insert"]):
        print("⚠️ Unsafe query blocked")
        continue

    chat_history.append({"role": "assistant", "content": sql_query})

    print("\nRunning query...")
    
    try:
        results = run_query(sql_query)

    except Exception as e:
        print("\nError detected. Fixing query...")

        fixed_query = fix_sql(user_input, sql_query, str(e))

        print("\nFixed SQL:")
        print(fixed_query)

        results = run_query(fixed_query)

    print("\nResults:")
    for row in results:
        print(row)