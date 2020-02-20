
from dotenv import load_dotenv
import os
import requests

invalid_call = """{
    \"Error Message\": \"Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.\"
}"""

load_dotenv()
API_key = os.environ.get("ALPHAVANTAGE_API_KEY","something isnt right")
print(API_key) 
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!") 
print("-------------------------") 
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

data = response.json()["Time Series (Daily)"]
print(response.status_code)
print(response.text)