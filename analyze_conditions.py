import csv
from collections import defaultdict

results = defaultdict(list)

with open(
    "ocr_condition_results.csv",
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        results[row["condition"]].append(row)

print("\nOCR CONDITION ANALYSIS")
print("=" * 65)
print(f"{'Condition':<15} {'Correct':<12} {'Accuracy':<12} {'Avg Time (s)'}")
print("-" * 65)

for condition, rows in results.items():
    total = len(rows)
    correct = sum(
        row["correct"].strip().lower() == "true"
        for row in rows
    )

    accuracy = (correct / total) * 100

    average_time = sum(
        float(row["processing_time_seconds"])
        for row in rows
    ) / total

    print(
        f"{condition:<15} "
        f"{correct}/{total:<10} "
        f"{accuracy:>6.1f}%      "
        f"{average_time:.4f}"
    )

print("\nAnalysis complete!")