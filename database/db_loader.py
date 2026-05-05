import re
import sqlite3
import pandas as pd

def clean_column_name(column_name: str) -> str:
    """
    Converts messy CSV column names into SQLite-safe column names.

    Example:
    'Order Date' -> 'order_date'
    'Total Sales ($)' -> 'total_sales'
    """
    column_name = column_name.strip().lower()
    column_name = re.sub(r"[^a-zA-Z0-9_]+", "_", column_name)
    column_name = re.sub(r"_+", "_", column_name)
    column_name = column_name.strip("_")

    if not column_name:
        column_name = "column"

    if column_name[0].isdigit():
        column_name = f"col_{column_name}"

    return column_name


def clean_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans dataframe column names and handles duplicates.
    """
    cleaned_df = df.copy()

    cleaned_columns = []
    seen_columns = {}

    for column in cleaned_df.columns:
        cleaned_column = clean_column_name(str(column))

        if cleaned_column in seen_columns:
            seen_columns[cleaned_column] += 1
            cleaned_column = f"{cleaned_column}_{seen_columns[cleaned_column]}"
        else:
            seen_columns[cleaned_column] = 0

        cleaned_columns.append(cleaned_column)

    cleaned_df.columns = cleaned_columns

    return cleaned_df


def create_sqlite_db_from_dataframe(
    df: pd.DataFrame,
    db_path: str,
    table_name: str,
) -> None:
    """
    Creates or replaces a SQLite table from an uploaded CSV dataframe.
    """
    cleaned_df = clean_dataframe_columns(df)

    conn = sqlite3.connect(db_path)

    try:
        cleaned_df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False,
        )
    finally:
        conn.close()
