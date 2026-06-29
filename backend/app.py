from flask import Flask, render_template, request
from predictor import predict_price
from data_fetcher import fetch_stock_data

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        # Get stock symbol from user
        stock = request.form["stock"]

        try:
            # Fetch latest stock features
            features = fetch_stock_data(stock)

            # AI Prediction
            prediction = predict_price(features)

            return f"""
            <h2>Stock: {stock}</h2>
            <h3>Tomorrow's Predicted Price: ₹{prediction:.2f}</h3>
            """

        except Exception as e:
            return f"<h3>Error: {e}</h3>"

    return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True)