import requests
# import pandas as pd
from requests.models import HTTPError


#Get the data in CSV format

# I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF
def getStockInfo(**kwargs):
    try:
      response = requests.get(
        "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?apikey={}&periodType={}&period={}&frequencyType={}"
          .format(kwargs.get("ticker"), kwargs.get("apiKey"), kwargs.get("periodType"), kwargs.get("period"), kwargs.get("frequencyType")))
    except HTTPError:
        print("We don't have your info")
    except Exception:
            print("Something Happened")
    
    
    print(response.json(), 'split')
"""
Get the data you want: Historical data
MACD stuff, RSI
Volume
Price

Put it into the dataframe
make sure the price is always one period ahead
and delete the info for the first and last periods
"""