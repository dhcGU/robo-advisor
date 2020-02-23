# -*- coding: utf-8 -*-


from dotenv import load_dotenv
import os
import requests
import csv
import json
from datetime import datetime

invalid_call = """{
    \"Error Message\": \"Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.\"
}"""

load_dotenv()
API_key = os.environ.get("ALPHAVANTAGE_API_KEY","something isnt right")

while True:
    while True:
        symbol = input("Enter a stock ticker to pull information and recommendation: ")
        if(len(symbol) < 1 or len(symbol) > 5):
            print("Sorry, that ticker is not valid. Please try again.")
        else:
            break
    symbol = symbol.upper()
    request_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_key}")
    if("Error Message" in response.text):
        print("Sorry, that was not a stock ticker. Please try again.")
        continue
    break
parsed_response = json.loads(response.text)
time_series = parsed_response["Time Series (Daily)"]

csv_name = str(symbol) + "_prices.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_name)
csv_columns = ["timestamp", "open", "high", "low", "close", "volume"]
for key in time_series.keys():
    time_series[key]["timestamp"] = key
with open(csv_file_path, "w+",newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for key in time_series.keys():
        daily_open = time_series[key]["1. open"]
        daily_high = time_series[key]["2. high"]
        daily_low = time_series[key]["3. low"]
        daily_close = time_series[key]["4. close"]
        daily_volume = time_series[key]["5. volume"]
        writer.writerow({"timestamp": key, "open": daily_open, "high": daily_high, "low": daily_low, "close": daily_close, "volume": daily_volume}) 
    csv_file.close()
    
    
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_day = list(time_series.keys())[0]
latest_close = float(time_series[latest_day]['4. close'])
recent_high = float(time_series[latest_day]['2. high'])
recent_low = float(time_series[latest_day]['3. low'])

for key in time_series.keys():
    day_high = float(time_series[key]['2. high'])
    day_low = float(time_series[key]['3. low'])
    if (day_high > recent_high):
        recent_high = day_high
    if(day_low < recent_low):
        recent_low = day_low

data = response.json()["Time Series (Daily)"]
print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: ${latest_close:.2f}")
print(f"RECENT HIGH: ${recent_high:.2f}")
print(f"RECENT LOW: ${recent_low:.2f}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!") 
print("-------------------------") 