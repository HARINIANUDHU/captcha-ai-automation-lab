import sqlite3
import pandas as pd

DB_NAME = "captcha_results.db"
OUTPUT_FILE = "powerbi_captcha_data.csv"

connection = sqlite3.connect(DB_NAME)

query = """
SELECT
    id,
    run_id,
    challenge_type,
    challenge,
    answer,
    result,
    execution_time,
    created_at
FROM experiments
ORDER BY id
"""

df = pd.read_sql_query(query, connection)

connection.close()

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Export complete!")
print(f"Rows exported: {len(df)}")
print(f"File created: {OUTPUT_FILE}")