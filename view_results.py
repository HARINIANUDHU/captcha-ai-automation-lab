
import sqlite3

connection = sqlite3.connect("captcha_results.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        challenge,
        result,
        execution_time,
        created_at
    FROM experiments
    ORDER BY id DESC
""")

rows = cursor.fetchall()

print("\nCAPTCHA EXPERIMENT HISTORY\n")

for row in rows:
    print(row)

cursor.execute("""
    SELECT
        COUNT(*),
        AVG(execution_time)
    FROM experiments
""")

total, average_time = cursor.fetchone()

print("\nTOTAL EXPERIMENTS:", total)
print("AVERAGE EXECUTION TIME:", round(average_time or 0, 2), "seconds")

connection.close()