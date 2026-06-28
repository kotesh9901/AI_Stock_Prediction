from flask import Flask, render_template, request
import yfinance as yf

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

        # Get stock symbol
        stock = request.form["stock"]

        # Download stock data
        df = yf.download(stock, period="5d")

        # Get latest closing price
        latest_price = float(df["Close"].iloc[-1].iloc[0])

        return f"""
        <html>
        <head>
            <title>Stock Result</title>
        </head>
        <body>
            <h2>Stock: {stock}</h2>
            <h3>Latest Closing Price: ₹{latest_price:.2f}</h3>
            <br>
            <a href="/predict">⬅ Back</a>
        </body>
        </html>
        """

    return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True)