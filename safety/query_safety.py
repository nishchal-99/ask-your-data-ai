import re


HIGH_RISK_KEYWORDS = [
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
]

MEDIUM_RISK_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "CREATE",
    "REPLACE",
    "VACUUM",
    "ATTACH",
    "DETACH",
]


def analyze_sql_risk(sql: str) -> dict:
    detected_keywords = []

    # Multiple statements are dangerous
    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
    if len(statements) > 1:
        return {
            "risk": "high",
            "keywords": ["MULTIPLE_STATEMENTS"],
            "message": "High risk: multiple SQL statements detected.",
        }

    for keyword in HIGH_RISK_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql, flags=re.IGNORECASE):
            detected_keywords.append(keyword)

    if detected_keywords:
        return {
            "risk": "high",
            "keywords": detected_keywords,
            "message": "High risk: this query may delete, remove, or alter database structure.",
        }

    for keyword in MEDIUM_RISK_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql, flags=re.IGNORECASE):
            detected_keywords.append(keyword)

    if detected_keywords:
        return {
            "risk": "medium",
            "keywords": detected_keywords,
            "message": "Medium risk: this query may modify the database.",
        }

    return {
        "risk": "safe",
        "keywords": [],
        "message": "Safe: this appears to be a read-only query.",
    }