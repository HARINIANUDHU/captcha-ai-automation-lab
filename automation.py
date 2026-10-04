
from playwright.sync_api import sync_playwright
import sqlite3
import re
import time

URL = "http://127.0.0.1:5000/"


def save_result(challenge, answer, result, duration):

    connection = sqlite3.connect("captcha_results.db")

    connection.execute("""
        INSERT INTO experiments
        (challenge_type, challenge, answer, result, execution_time)
        VALUES (?, ?, ?, ?, ?)
    """, ("math", challenge, str(answer), result, duration))

    connection.commit()
    connection.close()

    print("Experiment saved to database!")


def run_automation():

    start_time = time.perf_counter()

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(URL)

            challenge = page.locator("h3").inner_text()

            print("Challenge:", challenge)

            numbers = re.findall(r"\d+", challenge)

            answer = int(numbers[0]) + int(numbers[1])

            print("Calculated answer:", answer)

            page.locator("#answer").fill(str(answer))
            page.locator("#verify").click()

            page.get_by_text("CAPTCHA PASSED").wait_for()

            result = "SUCCESS"

        except Exception as error:
            result = "FAILED"
            print("Automation error:", error)

        duration = time.perf_counter() - start_time

        save_result(challenge, answer, result, duration)

        print("Result:", result)
        print(f"Execution time: {duration:.2f} seconds")

        page.wait_for_timeout(1500)
        browser.close()


if __name__ == "__main__":
    run_automation()