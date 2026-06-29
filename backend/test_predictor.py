from predictor import predict_price

# Sample stock values
features = [
    3300,      # Open
    3320,      # High
    3280,      # Low
    3310,      # Close
    2500000,   # Volume
    3250,      # MA_50
    3100       # MA_200
]

prediction = predict_price(features)

print("Tomorrow's Predicted Price:", prediction)