from PIL import Image, ImageDraw, ImageFont
import pytesseract
import time
import csv
from pathlib import Path

# Update this if Tesseract is installed in another location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Create a folder for generated test images
image_folder = Path("ocr_test_images")
image_folder.mkdir(exist_ok=True)

# Known text values for our controlled experiment
test_texts = [
    "4827",
    "1936",
    "7052",
    "8641",
    "3209",
    "5718",
    "2460",
    "9183",
    "6375",
    "1048"
]

results = []

for index, expected_text in enumerate(test_texts, start=1):
    # Generate a clean image containing the known text
    image = Image.new("RGB", (400, 150), "white")
    draw = ImageDraw.Draw(image)
    draw.text((100, 45), expected_text, fill="black")

    image_path = image_folder / f"sample_{index}.png"
    image.save(image_path)

    # Run OCR and measure processing time
    start_time = time.perf_counter()

    recognized_text = pytesseract.image_to_string(
        image,
        config="--psm 7 -c tessedit_char_whitelist=0123456789"
    ).strip()

    elapsed_time = time.perf_counter() - start_time

    correct = recognized_text == expected_text

    results.append({
        "sample_id": index,
        "expected_text": expected_text,
        "recognized_text": recognized_text,
        "correct": correct,
        "processing_time_seconds": round(elapsed_time, 4)
    })

    print(
        f"Sample {index}: expected={expected_text}, "
        f"recognized={recognized_text!r}, correct={correct}, "
        f"time={elapsed_time:.4f}s"
    )

# Save experiment results to a CSV file
csv_path = "ocr_results.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

correct_count = sum(row["correct"] for row in results)
accuracy = (correct_count / len(results)) * 100
average_time = sum(
    row["processing_time_seconds"] for row in results
) / len(results)

print("\n--- EXPERIMENT SUMMARY ---")
print(f"Total samples: {len(results)}")
print(f"Correct readings: {correct_count}")
print(f"Exact-match accuracy: {accuracy:.1f}%")
print(f"Average processing time: {average_time:.4f} seconds")
print(f"Results saved to: {csv_path}")