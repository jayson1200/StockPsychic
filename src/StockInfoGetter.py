import requests
import pandas as pd
from requests.models import HTTPError


#Get the data in CSV format

# I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF
def getStockInfo(**kwargs):
    try:
      response = requests.get(
        "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?apikey={}&periodType={}&period={}&frequencyType={}"
          .format(kwargs.get("ticker"), kwargs.get("apiKey"), kwargs.get("periodType"), kwargs.get("period"), kwargs.get("frequencyType")))

      print(type(response.json()))
    except HTTPError:
        print("We don't have your info")
    except Exception:
            print("Something Happened")
    
    data = response.json()

    data.pop("symbol")
    data.pop("empty")

    dataCandleList = data["candles"]

    
    stockInfoDF = pd.DataFrame(dataCandleList)
    print(stockInfoDF)

    return stockInfoDF

def calculateRSIData(stockDF):
    stockDF


    


"""
Get the data you want: Historical data
MACD , 
RSI: You will need to chop off the first 14 data points
Volume
Price

Put it into the dataframe
make sure the price is always one period ahead
and delete the info for the first and last periods
"""