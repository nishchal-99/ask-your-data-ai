import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_sql(sql_query: str, user_question: str) -> str:
    prompt = f"""
You are a helpful data analyst.

Explain the following SQL query in simple English.

User question:
{user_question}

SQL query:
{sql_query}

Rules:
- Keep it short.
- Use simple language.
- Explain what data is being selected, filtered, grouped, sorted, or limited.
- Do not mention technical SQL keywords unless necessary.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content.strip()