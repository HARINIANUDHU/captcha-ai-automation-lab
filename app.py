from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def captcha():
    if request.method == "POST":
        user_answer = request.form.get("answer")

        if user_answer == str(app.config["ANSWER"]):
            return """
            <h1>CAPTCHA PASSED ✅</h1>
            <p>You solved the test challenge.</p>
            """

        return """
        <h1>CAPTCHA FAILED ❌</h1>
        <p>Incorrect answer.</p>
        """

    number1 = random.randint(1, 20)
    number2 = random.randint(1, 20)

    app.config["ANSWER"] = number1 + number2

    return render_template(
        "captcha.html",
        challenge=f"{number1} + {number2}"
    )


if __name__ == "__main__":
    app.run(debug=True)