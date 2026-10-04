import csv
from collections import Counter

csv_path = "ocr_results.csv"

total = 0
correct_count = 0
errors = []

with open(csv_path, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total += 1

        expected = row["expected_text"]
        recognized = row["recognized_text"]
        is_correct = row["correct"].strip().lower() == "true"

        if is_correct:
            correct_count += 1
        else:
            errors.append((expected, recognized))

accuracy = (correct_count / total * 100) if total else 0

print("OCR DATASET ANALYSIS")
print("--------------------")
print(f"Total images: {total}")
print(f"Correct: {correct_count}")
print(f"Incorrect: {total - correct_count}")
print(f"Exact-match accuracy: {accuracy:.1f}%")

print("\nIncorrect readings:")
for expected, recognized in errors:
    print(f"Expected {expected} -> Recognized {recognized}")