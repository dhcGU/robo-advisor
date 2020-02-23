# -*- coding: utf-8 -*-


from dotenv import load_dotenv
import os
import requests
import csv
import json

invalid_call = """{
    \"Error Message\": \"Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.\"
}"""

load_dotenv()
API_key = os.environ.get("ALPHAVANTAGE_API_KEY","something isnt right")
print(API_key) 

while True:
    while True:
        symbol = input("Enter a stock ticker to pull information and recommendation: ")
        if(len(symbol) < 1 or len(symbol) > 5):
            print("Sorry, that ticker is not valid. Please try again.")
        else:
            break
    symbol = symbol.upper()
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_key}")
    if("Error Message" in response.text):
        print("Sorry, that was not a stock ticker. Please try again.")
        continue
    break
parsed_response = json.loads(response.text)
time_series = parsed_response["Time Series (Daily)"]
csv_name = "data/" + str(symbol) + "_prices.csv"
csv_columns = ["open", "high", "low", "close", "volume"]
f = open(csv_name, 'w+')
writer = csv.DictWriter(f, fieldnames=csv_columns)
writer.writeheader()
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_day = list(time_series.keys())[0]
latest_close = float(time_series[latest_day]['4. close'])
recent_high = float(time_series[latest_day]['2. high'])
recent_low = float(time_series[latest_day]['3. low'])



data = response.json()["Time Series (Daily)"]
print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
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