from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pytesseract
import time
import csv
import random
from pathlib import Path

from database import initialize_database, save_experiment


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

OUTPUT_DIR = Path("ocr_condition_images")
OUTPUT_DIR.mkdir(exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
run_timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

test_texts = ["4827", "1936", "7052", "8641", "3209"]

conditions = [
    "clean",
    "small_text",
    "blurred",
    "light_noise"
]


def make_image(text, condition, output_path):
    image = Image.new("RGB", (400, 150), "white")
    draw = ImageDraw.Draw(image)

    font_size = 40 if condition == "small_text" else 60

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    draw.text((100, 40), text, fill="black", font=font)

    if condition == "blurred":
        image = image.filter(
            ImageFilter.GaussianBlur(radius=1)
        )

    elif condition == "light_noise":
        pixels = image.load()
        random.seed(42)

        for _ in range(1500):
            x = random.randrange(image.width)
            y = random.randrange(image.height)
            shade = random.choice([220, 235, 245])
            pixels[x, y] = (shade, shade, shade)

    image.save(output_path)

    return image


# Make sure database exists
initialize_database()

results = []


# Run OCR experiments
for condition in conditions:

    for index, expected_text in enumerate(test_texts, start=1):

        image_path = OUTPUT_DIR / f"{condition}_{index}.png"

        image = make_image(
            expected_text,
            condition,
            image_path
        )

        start_time = time.perf_counter()

        recognized_text = pytesseract.image_to_string(
            image,
            config="--psm 7 -c tessedit_char_whitelist=0123456789"
        ).strip()

        elapsed_time = time.perf_counter() - start_time

        correct = recognized_text == expected_text

        save_experiment(
            challenge_type=f"ocr_{condition}",
            challenge=expected_text,
            answer=recognized_text,
            result="correct" if correct else "incorrect",
            execution_time=round(elapsed_time, 4)
        )

        results.append({
            "run_id": run_id,
            "run_timestamp": run_timestamp,
            "condition": condition,
            "expected_text": expected_text,
            "recognized_text": recognized_text,
            "correct": correct,
            "processing_time_seconds": round(elapsed_time, 4)
        })

        print(
            f"{condition:12} | expected={expected_text} "
            f"| got={recognized_text!r} | correct={correct}"
        )