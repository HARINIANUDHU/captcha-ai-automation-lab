import sqlite3

DB_NAME = "captcha_results.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

print("\n===== CAPTCHA DATABASE ANALYSIS =====")

# Total experiments
cursor.execute("""
    SELECT COUNT(*)
    FROM experiments
""")

total = cursor.fetchone()[0]

print(f"\nTotal experiments: {total}")


# Result summary
cursor.execute("""
    SELECT result, COUNT(*)
    FROM experiments
    GROUP BY result
""")

print("\nResult summary:")

for result, count in cursor.fetchall():
    print(f"{result}: {count}")


# Average execution time
cursor.execute("""
    SELECT AVG(execution_time)
    FROM experiments
""")

average_time = cursor.fetchone()[0]

if average_time is not None:
    print(f"\nAverage execution time: {average_time:.4f} seconds")


# Challenge type summary
cursor.execute("""
    SELECT challenge_type, COUNT(*)
    FROM experiments
    GROUP BY challenge_type
    ORDER BY challenge_type
""")

print("\nChallenge types:")

for challenge_type, count in cursor.fetchall():
    print(f"{challenge_type}: {count}")


# OCR-specific accuracy
cursor.execute("""
    SELECT
        COUNT(*),
        SUM(CASE WHEN result = 'correct' THEN 1 ELSE 0 END)
    FROM experiments
    WHERE challenge_type LIKE 'ocr_%'
""")

ocr_total, ocr_correct = cursor.fetchone()

print("\n===== OCR ANALYSIS =====")

print(f"OCR experiments: {ocr_total}")
print(f"OCR correct: {ocr_correct}")

if ocr_total:
    accuracy = (ocr_correct / ocr_total) * 100
    print(f"OCR accuracy: {accuracy:.2f}%")


connection.close()