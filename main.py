import yfinance as yf
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import base64
from statsmodels.tsa.arima.model import ARIMA


app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:5173"}})


def get_stock_data(stock_symbol, start_date, end_date):
   stock = yf.Ticker(stock_symbol)
   data = stock.history(start=start_date, end=end_date)
   return data


def arima_prediction(stock_symbol, start_date, end_date, forecast_steps=5):
   stock_data = get_stock_data(stock_symbol, start_date, end_date)
   if stock_data.empty:
       return "unknown", None, None, None  # Return None for predictions and plots if data is empty


   # Prepare the time series data
   prices = stock_data["Close"].values


   # Perform ARIMA modeling and forecasting
   order = (1, 0, 1)  # Replace with the appropriate order for your ARIMA model
   model = ARIMA(prices, order=order)
   model_fit = model.fit()


   # Forecast the stock prices
   forecast = model_fit.forecast(steps=forecast_steps)


   # Determine the trend based on forecasted prices
   trend = determine_trend(forecast)


   # Create and save a line plot of historical stock prices
   historical_plot_buffer = create_stock_price_plot(stock_data)


   # Create and save a line plot of predicted stock prices
   forecast_dates = pd.date_range(start=stock_data.index[-1], periods=forecast_steps, freq='B')
   forecast_df = pd.DataFrame({
       "Date": forecast_dates,
       "Forecast": forecast
   })
   predicted_plot_buffer = create_predicted_price_plot(forecast_df)


   # Convert the plot images to base64-encoded strings
   historical_plot_image_base64 = base64.b64encode(historical_plot_buffer.getvalue()).decode()
   predicted_plot_image_base64 = base64.b64encode(predicted_plot_buffer.getvalue()).decode()


   return trend, historical_plot_image_base64, predicted_plot_image_base64


def create_stock_price_plot(stock_data):
   # Create a line plot of historical stock prices
   plt.figure(figsize=(10, 6))
   plt.plot(stock_data.index, stock_data["Close"], label="Closing Price")
   plt.xlabel("Date")
   plt.ylabel("Price")
   plt.title("Historical Stock Prices")
   plt.legend()
   plt.xticks(rotation=45)
   plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # Format date on x-axis
   plt.tight_layout()


   # Save the plot to a BytesIO buffer
   buffer = io.BytesIO()
   plt.savefig(buffer, format="png")
   plt.clf()
   buffer.seek(0)


   return buffer


def create_predicted_price_plot(forecast_df):
   # Create a line plot of predicted stock prices
   plt.figure(figsize=(10, 6))
   plt.plot(forecast_df["Date"], forecast_df["Forecast"], label="Predicted Prices", linestyle='dashed', color='orange')
   plt.xlabel("Date")
   plt.ylabel("Price")
   plt.title("Predicted Stock Prices (ARIMA)")
   plt.legend()
   plt.xticks(rotation=45)
   plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))  # Format date on x-axis
   plt.tight_layout()


   # Save the plot to a BytesIO buffer
   buffer = io.BytesIO()
   plt.savefig(buffer, format="png")
   plt.clf()
   buffer.seek(0)


   return buffer


def determine_trend(forecast):
   # Determine the trend based on forecasted prices
   first_price = forecast[0]
   last_price = forecast[-1]


   if last_price > first_price:
       return "up"
   elif last_price < first_price:
       return "down"
   else:
       return "stagnant"


@app.route('/predict', methods=['POST'])
def predict():
   stock_symbol = request.json['stock']
   start_date = request.json['start_date']
   end_date = request.json['end_date']


   prediction, historical_plot_image_base64, predicted_plot_image_base64 = arima_prediction(stock_symbol, start_date, end_date)


   if historical_plot_image_base64 and predicted_plot_image_base64:
       return jsonify({
           "prediction": prediction,
           "historical_plot_image": historical_plot_image_base64,
           "predicted_plot_image": predicted_plot_image_base64
       })
   else:
       return jsonify({"prediction": prediction})


if __name__ == '__main__':
   app.run(port=5000)

