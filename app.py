import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.title("S&P 500 Stock Price Prediction")

# taking dataset
sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(period="max")

# removing index of time to avoid timezone-related errors
sp500_data.index = sp500_data.index.tz_convert(None)

# Preprocessing: keep only necessary columns
sp500_data = sp500_data[['Open', 'High', 'Low', 'Close', 'Volume']]

# Generate "Tomorrow" and "Target" columns for prediction
sp500_data["Tomorrow"] = sp500_data["Close"].shift(-1)
sp500_data["Target"] = (sp500_data["Tomorrow"] > sp500_data["Close"]).astype(int)

# Filter data to the last 10 years
start_date = datetime.now() - timedelta(days=10 * 365)
sp500_data_10y = sp500_data.loc[start_date:]

#  last 10 years' Close price
st.subheader("S&P 500 Close Prices (Last 10 Years)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sp500_data_10y.index, sp500_data_10y["Close"], label="Close Price")
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.set_title("S&P 500 Close Prices (Last 10 Years)")
ax.legend()
st.pyplot(fig)

# Prepare data for model training
sp500_data = sp500_data.dropna()
X = sp500_data[['Open', 'High', 'Low', 'Close', 'Volume']]
y = sp500_data["Target"]

# Split into train and test sets (use data before the last row for training)
X_train, y_train = X[:-1], y[:-1]
X_test = X[-1:]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make a prediction for tomorrow
prediction = model.predict(X_test)[0]


st.subheader("Prediction for Tomorrow")
if prediction == 1:
    st.write("The model predicts that the S&P 500 stock price will **increase** tomorrow.")
else:
    st.write("The model predicts that the S&P 500 stock price will **decrease** tomorrow.")
