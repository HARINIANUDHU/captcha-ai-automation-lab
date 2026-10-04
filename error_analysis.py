import sqlite3
import pandas as pd

DB_NAME = "captcha_results.db"

connection = sqlite3.connect(DB_NAME)

query = """
SELECT
    id,
    challenge_type,
    challenge,
    answer,
    result,
    execution_time,
    created_at
FROM experiments
WHERE challenge_type LIKE 'ocr_%'
ORDER BY id
"""

df = pd.read_sql_query(query, connection)

connection.close()

print("\n===== OCR ERROR ANALYSIS =====")

print(f"Total OCR experiments: {len(df)}")

correct = (df["result"] == "correct").sum()
incorrect = (df["result"] == "incorrect").sum()

print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")

if len(df) > 0:
    accuracy = correct / len(df) * 100
    print(f"Accuracy: {accuracy:.2f}%")

print("\n===== CONDITION SUMMARY =====")

summary = (
    df.groupby("challenge_type")
    .agg(
        tests=("id", "count"),
        correct=("result", lambda x: (x == "correct").sum()),
        average_time=("execution_time", "mean")
    )
    .reset_index()
)

summary["accuracy"] = (
    summary["correct"] / summary["tests"] * 100
)

print(summary.to_string(index=False))


print("\n===== INCORRECT OCR RECORDS =====")

errors = df[df["result"] == "incorrect"]

if errors.empty:
    print("No OCR errors found.")
else:
    print(
        errors[
            [
                "id",
                "challenge_type",
                "challenge",
                "answer",
                "execution_time"
            ]
        ].to_string(index=False)
    )