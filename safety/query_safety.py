import re

def analyze_sql_risk(sql: str) -> dict:
    """
    Detects whether generated SQL may modify or destroy data.

    This function does not block the query.
    It only returns a warning report for the UI.
    """
    risky_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "VACUUM",
        "ATTACH",
        "DETACH",
    ]

    detected_keywords = []

    for keyword in risky_keywords:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql, flags=re.IGNORECASE):
            detected_keywords.append(keyword)

    semicolon_count = sql.count(";")

    if semicolon_count > 1:
        detected_keywords.append("MULTIPLE_STATEMENTS")

    if detected_keywords:
        return {
            "risk": "warning",
            "keywords": detected_keywords,
            "message": "Warning: this SQL may modify the database or perform a sensitive operation.",
        }

    return {
        "risk": "safe",
        "keywords": [],
        "message": "This appears to be a read-only query.",
    }