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
WHERE challenge_type LIKE 'stress_%'
ORDER BY id
"""

df = pd.read_sql_query(query, connection)

connection.close()

print("\n===== CAPTCHA STRESS ANALYSIS =====")

print(f"\nTotal stress experiments: {len(df)}")

correct = (df["result"] == "correct").sum()
incorrect = (df["result"] == "incorrect").sum()

print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")

if len(df) > 0:
    accuracy = correct / len(df) * 100
    print(f"Accuracy: {accuracy:.2f}%")


print("\n===== CONDITION PERFORMANCE =====")

summary = (
    df.groupby("challenge_type")
    .agg(
        tests=("id", "count"),
        correct=("result", lambda x: (x == "correct").sum()),
        average_time=("execution_time", "mean")
    )
    .reset_index()
)

summary["incorrect"] = (
    summary["tests"] - summary["correct"]
)

summary["accuracy"] = (
    summary["correct"] / summary["tests"] * 100
)

summary["failure_rate"] = (
    summary["incorrect"] / summary["tests"] * 100
)

print(
    summary[
        [
            "challenge_type",
            "tests",
            "correct",
            "incorrect",
            "accuracy",
            "failure_rate",
            "average_time"
        ]
    ].to_string(index=False)
)


print("\n===== OCR OUTPUT ERRORS =====")

errors = df[df["result"] == "incorrect"]

if errors.empty:

    print("No errors found.")

else:

    print(
        errors[
            [
                "challenge_type",
                "challenge",
                "answer",
                "execution_time"
            ]
        ].to_string(index=False)
    )


print("\n===== OVERALL INSIGHT =====")

if len(df) > 0:

    slowest = summary.loc[
        summary["average_time"].idxmax()
    ]

    highest_failure = summary.loc[
        summary["failure_rate"].idxmax()
    ]

    print(
        f"Slowest condition: "
        f"{slowest['challenge_type']} "
        f"({slowest['average_time']:.4f}s)"
    )

    print(
        f"Highest failure rate: "
        f"{highest_failure['challenge_type']} "
        f"({highest_failure['failure_rate']:.2f}%)"
    )