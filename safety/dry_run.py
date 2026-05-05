import re


def build_delete_dry_run_query(sql: str) -> str | None:
    """
    Converts:
    DELETE FROM table_name WHERE condition;

    Into:
    SELECT COUNT(*) FROM table_name WHERE condition;
    """

    cleaned_sql = sql.strip().rstrip(";")

    pattern = r"DELETE\s+FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(WHERE\s+.+)?$"

    match = re.match(pattern, cleaned_sql, flags=re.IGNORECASE | re.DOTALL)

    if not match:
        return None

    table_name = match.group(1)
    where_clause = match.group(2)

    if where_clause:
        return f"SELECT COUNT(*) AS affected_rows FROM {table_name} {where_clause};"

    return f"SELECT COUNT(*) AS affected_rows FROM {table_name};"