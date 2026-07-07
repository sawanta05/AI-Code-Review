from flask import Flask, request, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Code Review Backend Running"

@app.route("/review", methods=["POST"])
def review_code():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    code = data.get("code")

    if not code:
        return jsonify({"error": "Code is missing"}), 400

    os.makedirs("temp", exist_ok=True)

    filename = "temp/temp_code.py"

    with open(filename, "w") as file:
        file.write(code)

    result = subprocess.run(
    [sys.executable, "-m", "pylint", filename],
    capture_output=True,
    text=True
)

    return jsonify({
    "review": result.stdout,
    "return_code": result.returncode
})
if __name__ == "__main__":
    app.run(debug=False)