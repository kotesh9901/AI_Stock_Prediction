import joblib

# Load AI Model
model = joblib.load("models/stock_model.pkl")

def predict_price(features):

    # features is already a list:
    # [Open, High, Low, Close, Volume, MA_50, MA_200]

    prediction = model.predict([features])

    # Return predicted price
    return float(prediction.ravel()[0])