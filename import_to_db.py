import sqlite3
import pandas as pd

# Connect to database (creates it if not exists)
conn = sqlite3.connect("data.db")

# Read CSV
df = pd.read_csv("sales_data.csv")

# Load into database
df.to_sql("sales_data", conn, if_exists="replace", index=False)

conn.close()

print("Data imported successfully into SQLite database!")
