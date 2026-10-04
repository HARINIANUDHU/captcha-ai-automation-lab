from PIL import Image, ImageDraw
import pytesseract
import time

# Tell Python where the Tesseract application is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Known text in our generated test image
expected_text = "4827"

# Create a simple test image
image = Image.new("RGB", (400, 150), color="white")
draw = ImageDraw.Draw(image)
draw.text((100, 45), expected_text, fill="black")

# Save the image
image.save("ocr_test.png")

# Run OCR and measure processing time
start_time = time.perf_counter()

recognized_text = pytesseract.image_to_string(
    image,
    config="--psm 7 -c tessedit_char_whitelist=0123456789"
).strip()

elapsed_time = time.perf_counter() - start_time

# Compare result with known text
correct = recognized_text == expected_text

print("Expected text:", expected_text)
print("OCR recognized:", repr(recognized_text))
print("Correct:", correct)
print(f"OCR time: {elapsed_time:.4f} seconds")
print("Image saved as ocr_test.png")