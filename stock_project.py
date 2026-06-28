import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ==========================
# Download Stock Data
# ==========================

stock = "TCS.NS"

df = yf.download(stock, start="2020-01-01", end="2025-01-01")

print(df.head())

df.to_csv("stock_data.csv")

# ==========================
# Moving Averages
# ==========================

df = df.dropna()

df["MA_50"] = df["Close"].rolling(50).mean()
df["MA_200"] = df["Close"].rolling(200).mean()

df = df.dropna()

# ==========================
# Graph
# ==========================

plt.figure(figsize=(12,6))

plt.plot(df["Close"], label="Close Price")
plt.plot(df["MA_50"], label="50 Day MA")
plt.plot(df["MA_200"], label="200 Day MA")

plt.title("TCS Stock Analysis")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()

plt.show()

# ==========================
# Machine Learning
# ==========================

# Features
X = df[["Open","High","Low","Close","Volume","MA_50","MA_200"]]

# Target (Tomorrow Close)
y = df["Close"].shift(-1)

# Remove last row
X = X[:-1]
y = y[:-1]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = LinearRegression()

# Train Model
model.fit(X_train, y_train)

# Prediction
prediction = model.predict(X_test)

# Accuracy
rmse = mean_squared_error(y_test, prediction)

print("\nModel Trained Successfully!")
print("RMSE:", rmse)

print("\nFirst 10 Predictions")

# Convert to 1-dimensional arrays
actual = y_test.squeeze()
predicted = prediction.squeeze()

results = pd.DataFrame({
    "Actual": actual,
    "Predicted": predicted
})

print(results.head(10))
print(results.head(10))

# ==========================
# Prediction Graph
# ==========================

plt.figure(figsize=(12,6))

plt.plot(y_test.values[:100], label="Actual Price")
plt.plot(prediction[:100], label="Predicted Price")

plt.title("Actual vs Predicted Stock Price")
plt.xlabel("Days")
plt.ylabel("Price")

plt.legend()
plt.grid()

plt.show()
import joblib

# Save the trained model
joblib.dump(model, "models/stock_model.pkl")

print("Model saved successfully!")
# ==============================
# Load Saved Model
# ==============================

loaded_model = joblib.load("models/stock_model.pkl")

print("\nSaved model loaded successfully!")