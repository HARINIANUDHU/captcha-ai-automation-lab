import sqlite3

DB_NAME = "captcha_results.db"

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
ORDER BY id DESC
LIMIT 10
"""

rows = connection.execute(query).fetchall()

connection.close()

print("\n========== LATEST 10 RECORDS ==========\n")

for row in rows:
    print(
        f"ID={row[0]} "
        f"| Run ID={row[1]} "
        f"| Type={row[2]} "
        f"| Expected={row[3]} "
        f"| OCR={row[4]} "
        f"| Result={row[5]} "
        f"| Time={row[6]}s "
        f"| Created={row[7]}"
    )