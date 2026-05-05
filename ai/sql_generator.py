import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_sql(sql: str) -> str:
    """
    Removes markdown formatting from AI output.
    """
    if not sql:
        return ""

    sql = sql.strip()
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


def generate_sql(
    user_input: str,
    schema_description: str,
    table_name: str,
) -> str:
    """
    Converts English questions into SQLite SQL using the uploaded CSV schema.
    """
    prompt = f"""
You are a senior data analyst writing SQL for SQLite.

The user uploaded a CSV file. It has been loaded into SQLite.

Use this exact table name:
{table_name}

Database schema:
{schema_description}

Rules:
- Return ONLY raw SQL.
- Do NOT include markdown.
- Do NOT explain the SQL.
- Use SQLite syntax only.
- Use only the provided table and columns.
- Do not invent tables.
- Do not invent columns.
- Prefer SELECT queries unless the user clearly asks to modify, update, insert, or delete data.
- If the user asks to view, show, list, compare, summarize, count, average, group, rank, sort, find, filter, or analyze data, use SELECT.
- If the user asks "top", "highest", "best", "most", or "largest", sort DESC.
- If the user asks "least", "lowest", "worst", "bottom", or "smallest", sort ASC.
- If the user asks for a trend, group by a date/time column if one exists.
- If column names contain underscores, use them exactly as shown in the schema.
- Do not wrap table names or column names in backticks unless necessary.
- Do not use comments.

User question:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    sql = response.choices[0].message.content
    return clean_sql(sql)
