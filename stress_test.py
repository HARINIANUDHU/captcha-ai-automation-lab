from PIL import Image, ImageDraw, ImageFilter
import pytesseract
import random
import time
import sqlite3


# =========================================
# CONFIGURATION
# =========================================

DB_NAME = "captcha_results.db"

# Automatically create a unique Run ID
RUN_ID = "RUN-" + time.strftime("%Y%m%d-%H%M%S")

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================================
# DATABASE: ENSURE RUN_ID COLUMN EXISTS
# =========================================

def ensure_run_id_column():

    connection = sqlite3.connect(DB_NAME)

    columns = connection.execute(
        "PRAGMA table_info(experiments)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "run_id" not in column_names:

        connection.execute("""
            ALTER TABLE experiments
            ADD COLUMN run_id TEXT
        """)

        connection.commit()

        print("run_id column added successfully!")

    else:

        print("run_id column already exists.")

    connection.close()


# =========================================
# SAVE RESULT TO DATABASE
# =========================================

def save_result(condition, expected, recognized, execution_time):

    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO experiments
        (
            run_id,
            challenge_type,
            challenge,
            answer,
            result,
            execution_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        RUN_ID,
        f"stress_{condition}",
        expected,
        recognized,
        "correct" if expected == recognized else "incorrect",
        execution_time
    ))

    connection.commit()
    connection.close()


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

    # Draw characters with different positions
    x = 45

    for char in text:

        y = random.randint(15, 40)

        draw.text(
            (x, y),
            char,
            fill="black"
        )

        x += 45


    # =====================================
    # APPLY SYNTHETIC CONDITIONS
    # =====================================

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
# TEST CONDITIONS
# =========================================

conditions = [
    "heavy_blur",
    "heavy_noise",
    "low_contrast",
    "lines",
    "distorted"
]


# =========================================
# TEST DATA
# =========================================

texts = [
    "4827",
    "1936",
    "7052",
    "8641",
    "3209"
]


# =========================================
# MAIN PROGRAM
# =========================================

# Make sure database has run_id column
ensure_run_id_column()


print("\n=========================================")
print("      CAPTCHA OCR STRESS TEST")
print("=========================================")

print(f"\nRUN ID: {RUN_ID}")

print("\nStarting 25 tests...\n")


# =========================================
# RUN ALL TESTS
# =========================================

for condition in conditions:

    print(
        f"\n--- {condition.upper()} ---"
    )

    for expected_text in texts:

        # Create CAPTCHA
        image = create_captcha(
            expected_text,
            condition
        )


        # Start timer
        start_time = time.perf_counter()


        # OCR
        recognized_text = pytesseract.image_to_string(
            image,
            config="--psm 8"
        ).strip()


        # Calculate execution time
        execution_time = (
            time.perf_counter() - start_time
        )


        # Check result
        correct = (
            recognized_text == expected_text
        )


        # Save to database
        save_result(
            condition,
            expected_text,
            recognized_text,
            round(execution_time, 4)
        )


        # Display result
        print(
            f"Expected={expected_text} "
            f"| OCR={recognized_text!r} "
            f"| Correct={correct} "
            f"| Time={execution_time:.4f}s"
        )


# =========================================
# COMPLETE
# =========================================

print("\n=========================================")
print("       STRESS TEST COMPLETE")
print("=========================================")

print(f"\nRun ID: {RUN_ID}")

print("Tests completed: 25")

print("\nAll results saved to database.")