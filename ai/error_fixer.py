import os

from dotenv import load_dotenv
from openai import OpenAI

from ai.sql_generator import clean_sql

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fix_sql(
    user_question: str,
    failed_sql: str,
    error_message: str,
    schema_description: str,
    table_name: str,
) -> str:
    prompt = f"""
You are a senior SQLite expert.

The previous SQL query failed.

User question:
{user_question}

Table name:
{table_name}

Database schema:
{schema_description}

Failed SQL:
{failed_sql}

SQLite error:
{error_message}

Your task:
- Return ONLY the corrected SQL.
- Do NOT include markdown.
- Do NOT explain.
- Use SQLite syntax only.
- Use only the provided table and columns.
- Do not invent columns or tables.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return clean_sql(response.choices[0].message.content)