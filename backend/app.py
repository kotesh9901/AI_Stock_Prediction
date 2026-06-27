from flask import Flask

# Create Flask application
app = Flask(__name__)

# Home Page Route
@app.route("/")
def home():
    return """
    <h1>🚀 AI-Based Intelligent Stock Prediction System</h1>
    <h2>Backend Running Successfully</h2>
    <p>Welcome Kotesh!</p>
    <p>This is our AI + DevOps Final Year Project.</p>
    """

# Run the application
if __name__ == "__main__":
    app.run(debug=True)