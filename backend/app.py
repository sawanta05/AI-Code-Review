from flask import Flask

# Create Flask application
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "AI Code Review Backend Running"

# Run server
if __name__ == "__main__":
    app.run(debug=True)