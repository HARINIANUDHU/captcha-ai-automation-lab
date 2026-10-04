from PIL import Image, ImageDraw, ImageFilter, ImageOps
import pytesseract
import random
import time


# =========================================
# TESSERACT
# =========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================================
# CREATE SYNTHETIC CAPTCHA
# =========================================

def create_captcha(text, condition):

    image = Image.new(
        "RGB",
        (300, 100),
        "white"
    )

    draw = ImageDraw.Draw(image)

    x = 45

    for char in text:

        y = random.randint(15, 40)

        draw.text(
            (x, y),
            char,
            fill="black"
        )

        x += 45


    # Apply difficult condition

    if condition == "heavy_blur":

        image = image.filter(
            ImageFilter.GaussianBlur(3)
        )


    elif condition == "heavy_noise":

        pixels = image.load()

        for _ in range(5000):

            x = random.randint(0, 299)
            y = random.randint(0, 99)

            pixels[x, y] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )


    elif condition == "low_contrast":

        image = image.convert("L")

        image = image.point(
            lambda p: 120 if p > 180 else 80
        )


    elif condition == "lines":

        for _ in range(12):

            draw.line(
                (
                    random.randint(0, 300),
                    random.randint(0, 100),
                    random.randint(0, 300),
                    random.randint(0, 100)
                ),
                fill="gray",
                width=2
            )


    elif condition == "distorted":

        image = image.rotate(
            random.randint(-15, 15),
            expand=False,
            fillcolor="white"
        )


    return image


# =========================================
# ORIGINAL OCR
# =========================================

def original_ocr(image):

    result = pytesseract.image_to_string(
        image,
        config="--psm 8"
    ).strip()

    return result


# =========================================
# PREPROCESSING
# =========================================

def preprocess_image(image):

    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase contrast
    gray = ImageOps.autocontrast(gray)

    # Convert to black and white
    threshold = gray.point(
        lambda p: 0 if p < 160 else 255
    )

    # Resize image
    threshold = threshold.resize(
        (600, 200)
    )

    return threshold


# =========================================
# IMPROVED OCR
# =========================================

def improved_ocr(image):

    processed = preprocess_image(image)

    result = pytesseract.image_to_string(
        processed,
        config="--psm 8"
    ).strip()

    return result


# =========================================
# TEST DATA
# =========================================

conditions = [
    "heavy_blur",
    "heavy_noise",
    "low_contrast",
    "lines",
    "distorted"
]

texts = [
    "4827",
    "1936",
    "7052",
    "8641",
    "3209"
]


# =========================================
# MAIN EXPERIMENT
# =========================================

print("\n=========================================")
print("       OCR IMPROVEMENT EXPERIMENT")
print("=========================================\n")


total_original = 0
correct_original = 0

total_improved = 0
correct_improved = 0


for condition in conditions:

    print(
        f"\n========== {condition.upper()} =========="
    )

    for expected in texts:

        image = create_captcha(
            expected,
            condition
        )


        # -------------------------------
        # ORIGINAL OCR
        # -------------------------------

        start = time.perf_counter()

        original_result = original_ocr(image)

        original_time = (
            time.perf_counter() - start
        )

        original_correct = (
            original_result == expected
        )


        # -------------------------------
        # IMPROVED OCR
        # -------------------------------

        start = time.perf_counter()

        improved_result = improved_ocr(image)

        improved_time = (
            time.perf_counter() - start
        )

        improved_correct = (
            improved_result == expected
        )


        # -------------------------------
        # COUNTERS
        # -------------------------------

        total_original += 1
        total_improved += 1

        if original_correct:
            correct_original += 1

        if improved_correct:
            correct_improved += 1


        # -------------------------------
        # DISPLAY
        # -------------------------------

        print(
            f"Expected={expected} "
            f"| Original={original_result!r} "
            f"| Improved={improved_result!r} "
            f"| Before={original_correct} "
            f"| After={improved_correct} "
            f"| Time={improved_time:.4f}s"
        )


# =========================================
# FINAL RESULTS
# =========================================

original_accuracy = (
    correct_original / total_original
) * 100


improved_accuracy = (
    correct_improved / total_improved
) * 100


print("\n=========================================")
print("             FINAL RESULTS")
print("=========================================")

print(
    f"\nOriginal OCR Accuracy : "
    f"{original_accuracy:.2f}%"
)

print(
    f"Improved OCR Accuracy : "
    f"{improved_accuracy:.2f}%"
)

print(
    f"\nImprovement : "
    f"{improved_accuracy - original_accuracy:.2f} percentage points"
)

print("\n=========================================")
print("       EXPERIMENT COMPLETE")
print("=========================================")