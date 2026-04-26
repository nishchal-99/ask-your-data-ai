import sqlite3

import pandas as pd


CSV_PATH = "sales_data.csv"
DB_PATH = "data.db"
TABLE_NAME = "sales_data"


def import_csv_to_sqlite():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)

    try:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        print(f"Imported {len(df)} rows into table '{TABLE_NAME}'.")

    finally:
        conn.close()


if __name__ == "__main__":
    import_csv_to_sqlite()