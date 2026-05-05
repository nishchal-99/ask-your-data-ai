import pandas as pd
from database.db_loader import clean_dataframe_columns


def get_schema_description(
    df: pd.DataFrame,
    table_name: str,
) -> str:
    cleaned_df = clean_dataframe_columns(df)

    schema_lines = [f"Table: {table_name}", "", "Columns:"]

    for column in cleaned_df.columns:
        dtype = str(cleaned_df[column].dtype)
        schema_lines.append(f"- {column} ({dtype})")

    return "\n".join(schema_lines)