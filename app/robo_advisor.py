# -*- coding: utf-8 -*-


from dotenv import load_dotenv
import os
import requests
import csv
import json
from datetime import datetime
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import seaborn as sns
import matplotlib.pyplot as plt

request_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

def hasNumber(string):
    return any(ch.isdigit() for ch in string)

def render_email(symbol, change):
    html = "<div><br>"
    html += "<b>Alert!</b><br>"
    html += f"{symbol}\'s price has swung by {change*100:.2f}% in the past day!<br>"
    html += f"Search for {symbol} with Robo Advisor for more information and a recommendation.<br>"
    html += "</div>"
    return html

invalid_call = """{
    \"Error Message\": \"Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.\"
}"""

load_dotenv()
API_key = os.environ.get("ALPHAVANTAGE_API_KEY","something isnt right")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY","missing sendgrid api key")
email = ""
print("Welcome to Robo Advisor, a tool for stock research and recommendations!")
while True:
    answer = input("Would you like to receive automatic alerts about large changes in the stocks you research? (y/n)\n")
    if (answer.lower() == 'y'):
        email = input('What is your email address?\n')
        break
    elif(answer.lower() == 'n'):
        break
    else:
        print("Sorry, I didn't understant that. Please enter \'y\' or \'n\'")
print("Note: Once a valid stock ticker is entered, a line graph of its price over the past 100 days will open in a new window.")
print("To proceed to the stocks information and recommendation, that window must be closed.")
while True:
    while True:
        symbol = input("Enter a stock ticker to pull information and recommendation: ")
        if(len(symbol) < 1 or len(symbol) > 5 or hasNumber(symbol)):
            print("Sorry, that ticker is not valid. Please try again. Most stock tickers are all letters and 1-5 characters long.")
        else:
            break
    symbol = symbol.upper()
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_key}")
    weekly_response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_key}")
    if("Error Message" in response.text):
        print("Sorry, that was not a stock ticker. Please try again.")
        continue
    break
parsed_response = json.loads(response.text)
weekly_parsed_response = json.loads(weekly_response.text)

time_series = parsed_response["Time Series (Daily)"]
weekly_time_series = weekly_parsed_response["Weekly Time Series"]

csv_name = "data/" + str(symbol) + "_prices.csv"

csv_columns = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_name, "w+",newline="") as csv_file:
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

pandas_data = pd.read_csv(csv_name)
pandas_data['%change'] = (pandas_data['close']-pandas_data['open'])/pandas_data['open']

x = pandas_data.iloc[:-1,1:6]
y = pandas_data.iloc[1:,6]
y_true = pd.Series(y > 0)

x_train, x_test, y_train, y_test = train_test_split(x, y_true, test_size = 0.3, random_state=324)
increasing_price_classifier = DecisionTreeClassifier(max_leaf_nodes = 15, random_state = 10)
increasing_price_classifier.fit(x_train,y_train)
test_predictions = increasing_price_classifier.predict(x_test)
acc_score = accuracy_score(y_true=y_test, y_pred=test_predictions)


to_predict = pandas_data.iloc[1:,1:6]
real_predictions = increasing_price_classifier.predict(to_predict)
tomorrows_prediction = real_predictions[-1]
if(tomorrows_prediction == True):
    recommendation = "Buy!"
    direction = "increase"
else:
    recommendation = "Do not buy/Sell!"
    direction = "decrease"

price_plot = sns.lineplot(pandas_data["timestamp"], pandas_data["close"])
price_plot.set(xlabel="Days",ylabel="Closing Price (USD)")
price_plot.set_title(f"{symbol} Price Over Past 100 Days")
price_plot.set(xticklabels=[])
plt.show()

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_day = list(time_series.keys())[0]
latest_close = float(time_series[latest_day]['4. close'])
recent_high = float(time_series[latest_day]['2. high'])
recent_low = float(time_series[latest_day]['3. low'])


recent_change = (recent_high - recent_low)/recent_low
if(recent_change > 0.05):
    if(email != ""):
        client = SendGridAPIClient(SENDGRID_API_KEY)
        subject = f"{symbol} Price Movements from Robo Banking Advisor"
        content = render_email(symbol, recent_change)
        message = Mail(from_email="Advisor@Robo.ai", to_emails=email,subject=subject,html_content=content)
        try:
            client.send(message)
        except:
            print("",end="") #ignore bad email addresses

for key in time_series.keys():
    day_high = float(time_series[key]['2. high'])
    day_low = float(time_series[key]['3. low'])
    if (day_high > recent_high):
        recent_high = day_high
    if(day_low < recent_low):
        recent_low = day_low

fiftytwo_week_high = recent_high
fiftytwo_week_low = recent_low

weekly_keys = list(weekly_time_series.keys())
Min_of_52_and_available_information = min([52,len(weekly_keys)])

for i in range(Min_of_52_and_available_information):
    week_high = float(weekly_time_series[weekly_keys[i]]['2. high'])
    week_low = float(weekly_time_series[weekly_keys[i]]['3. low'])
    if (week_high > fiftytwo_week_high):
        fiftytwo_week_high = week_high
    if(week_low < fiftytwo_week_low):
        fiftytwo_week_low = week_low



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
print(f"52 WEEK HIGH: ${fiftytwo_week_high:.2f}")
print(f"52 WEEK LOW: ${fiftytwo_week_low:.2f}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print("RECOMMENDATION REASON: " + f"""\nOur machine learning algorithm analyzed {symbol}'s price changes for the past 100 days.
It used a Decision Tree Classifier to predict its returns with {acc_score*100:.2f}% accuracy and expects its price to {direction} tomorrow!""")
print("-------------------------")
print("HAPPY INVESTING!") 
print("-------------------------") 

