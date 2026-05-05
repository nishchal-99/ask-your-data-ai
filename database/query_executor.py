import sqlite3
from typing import Optional


def run_query(
    query: str,
    db_path: str,
    params: Optional[tuple] = None,
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
        else:
            conn.commit()
            columns = []
            results = []

        return columns, results

    finally:
        conn.close()