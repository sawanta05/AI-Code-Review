from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Code Review Backend Running"

@app.route("/review", methods=["POST"])
def review_code():

    data = request.get_json()

    code = data.get("code")

    return jsonify({
        "message": "Code received successfully!",
        "received_code": code
    })

if __name__ == "__main__":
    app.run(debug=True)