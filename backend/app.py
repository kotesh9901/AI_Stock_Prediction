from flask import Flask, render_template, request, session
from predictor import predict_price
from data_fetcher import fetch_stock_data
import sqlite3
import datetime

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "nutty_ai_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database/stock.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            session["email"] = email
            session["name"] = user[1]   # Store user's name

            return render_template(
                "dashboard.html",
                name=session["name"]
            )

        else:
            return "<h3>❌ Invalid Email or Password</h3>"

    return render_template("login.html")
# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "<h3>❌ Passwords do not match!</h3>"

        connection = sqlite3.connect("database/stock.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        connection.commit()
        connection.close()

        return """
        <h2>✅ Registration Successful!</h2>
        <br>
        <a href="/login">Go to Login</a>
        """

    return render_template("signup.html")


# ---------------- DASHBOARD ----------------
# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return render_template("login.html")

    return render_template(
        "dashboard.html",
        name=session["name"]
    )


# ---------------- HISTORY ----------------
@app.route("/history")
def history():

    connection = sqlite3.connect("database/stock.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT stock,
               predicted_price,
               prediction_date
        FROM predictions
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        history=history
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return render_template("index.html")


# ---------------- PREDICT ----------------
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        stock = request.form["stock"]

        try:

            # Get latest stock features
            features = fetch_stock_data(stock)

            # Current Closing Price
            current_price = features[3]

            # AI Prediction
            prediction = float(predict_price(features))

            # Difference
            difference = prediction - current_price

            # Trend
            if difference > 0:
                trend = "📈 Bullish"
            else:
                trend = "📉 Bearish"

            # Save Prediction
            connection = sqlite3.connect("database/stock.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO predictions
                (stock, predicted_price, prediction_date, user_email)
                VALUES (?, ?, ?, ?)
            """, (
                stock,
                prediction,
                datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                session["email"]
            ))

            connection.commit()
            connection.close()

            return render_template(
            "result.html",
            stock=stock,
            current_price=round(current_price, 2),
            prediction=round(prediction, 2),
            difference=round(difference, 2),
            trend=trend
)

        except Exception as e:
            return f"<h3>Error: {e}</h3>"

    return render_template("predict.html")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)