from flask import Flask, request, jsonify
import subprocess
import os
import sys
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Code Review Backend Running"

def parse_pylint_output(output):

    issues = []

    score = "Not Available"

    score_match = re.search(r"rated at ([0-9.]+/10)", output)

    if score_match:
        score = score_match.group(1)

    pattern = r".*temp_code\.py:(\d+):\d+:\s([A-Z]\d+):\s(.*)\s\((.*)\)"

    matches = re.findall(pattern, output)

    for match in matches:

        line = int(match[0])

        code = match[1]

        message = match[2]

        issue_type = match[3]

        issues.append({

            "line": line,

            "code": code,

            "type": issue_type,

            "message": message

        })

    return {

        "score": score,

        "issues": issues

    }

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

    print(result.stdout)
    
    parsed_review = parse_pylint_output(result.stdout)

    return jsonify(parsed_review)
if __name__ == "__main__":
    app.run(debug=False)