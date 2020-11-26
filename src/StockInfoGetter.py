import requests
import pandas as pd
from requests.models import HTTPError


#Get the data in CSV format

# I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF

#Gets the stock historical data and returns a dataframe
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
    #print(stockInfoDF)

    return stockInfoDF


# Calculates the RSI change data
def calculateRSIData(stockDF):
  #print(stockDF)

  upChangeList = [] 
  downChangeList = []

  rsiList = [1 for x in range(14)]

  # Creates the Up and down change values
  for x in range(len(stockDF.index+1)):
    if(x == 0):
      downChangeList.append(0)
      upChangeList.append(0)
    elif((stockDF.at[x, "close"] - stockDF.at[x-1, "close"]) < 0):
      downChangeList.append(stockDF.at[x, "close"] - stockDF.at[x-1, "close"])
      upChangeList.append(0)
    elif((stockDF.at[x, "close"] - stockDF.at[x-1, "close"]) > 0):
      downChangeList.append(0)
      upChangeList.append(stockDF.at[x, "close"] - stockDF.at[x-1, "close"])
    elif((stockDF.at[x, "close"] - stockDF.at[x-1, "close"]) == 0):
      downChangeList.append(0)
      upChangeList.append(0)

  
  stockDF.insert(6, "change up", upChangeList, True)
  stockDF.insert(7, "change down", downChangeList, True)

  # Adds all of the change value--up and down--for the past 14 periods and calculate RSI from it
  for i in range(14, len(stockDF.index+1)):
    avgUp = 0.0 
    avgDown = 0.0
    for j in range(i-14, i+1):
      avgUp += stockDF.at[j, "change up"]
      avgDown -= stockDF.at[j, "change down"]

    avgUp = avgUp/14
    avgDown = avgDown/14
    rsiList.append((100 - (100 / ( 1 + (avgUp/abs(avgDown))))))
      

  stockDF.insert(8, "RSI", rsiList, True)

  #print(stockDF.tail(28))
  print(stockDF)


    


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