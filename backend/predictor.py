import joblib

# Load AI model
model = joblib.load("models/stock_model.pkl")

def predict_price(features):
    """
    Predict tomorrow's stock price
    """
    prediction = model.predict([features])

    # Return the single prediction value
    return prediction.flatten()[0]