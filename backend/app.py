from datetime import datetime
import time
from flask_cors import CORS
from flask import Flask, request, jsonify
import subprocess
import os
import sys
import re

from dotenv import load_dotenv
from google import genai

app = Flask(__name__)
CORS(app)

from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")
print("Gemini Key:", os.getenv("GEMINI_API_KEY"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return "AI Code Review Backend Running"

def parse_pylint_output(output):

    issues = []

    summary = {
        "Convention": 0,
        "Warning": 0,
        "Error": 0,
        "Refactor": 0
    }

    score = "Not Available"

    score_match = re.search(r"rated at ([0-9.]+/10)", output)

    if score_match:
        score = score_match.group(1)

    pattern = r".*temp_code\.py:(\d+):\d+:\s([A-Z]\d+):\s(.*)\s\((.*)\)"

    matches = re.findall(pattern, output, re.MULTILINE)
    
    for match in matches:

        line = int(match[0])
        code = match[1]
        message = match[2]
        issue_type = match[3]

        if code.startswith("C"):
            summary["Convention"] += 1

        elif code.startswith("W"):
            summary["Warning"] += 1

        elif code.startswith("E"):
            summary["Error"] += 1

        elif code.startswith("R"):
            summary["Refactor"] += 1

        issues.append({
            "line": line,
            "code": code,
            "type": issue_type,
            "message": message
        })

    return {
        "score": score,
        "total_issues": len(issues),
        "summary": summary,
        "issues": issues
    }


def get_ai_review(code):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are an expert Python code reviewer.

Analyze the following Python code.

Respond in exactly this format:

## Overall Feedback

## Bugs

## Code Quality

## Best Practices

## Optimized Code

Keep your answers concise and beginner-friendly.

Python Code:
{code}
"""
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return str(e)
    
@app.route("/review", methods=["POST"])
def review_code():

    start_time = time.time()

    data = request.get_json()

    print("Received JSON:", data)

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    code = data.get("code")

    if not code:
        return jsonify({"error": "Code is missing"}), 400

    os.makedirs("temp", exist_ok=True)

    filename = "temp/temp_code.py"

    with open(filename, "w") as file:
        file.write(code)

        print("Python Executable:", sys.executable)

    result = subprocess.run(
    [sys.executable, "-m", "pylint", filename],
    capture_output=True,
    text=True
)

    print("Pylint Return Code:", result.returncode)
    print("STDERR:", result.stderr)

    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)
    
    parsed_review = parse_pylint_output(result.stdout)

    ai_review = get_ai_review(code)

    parsed_review["ai_review"] = ai_review

    parsed_review["reviewed_at"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    parsed_review["response_time"] = round(time.time() - start_time, 2)

    return jsonify(parsed_review)

if __name__ == "__main__":
    app.run(debug=False)