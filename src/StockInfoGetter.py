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
      avgDown += stockDF.at[j, "change down"]

    avgUp = avgUp/14
    avgDown = avgDown/14
    rsiList.append((100 - (100 / ( 1 + (avgUp/abs(avgDown))))))
      

  stockDF.insert(8, "RSI", rsiList, True)

  return stockDF

#Calculates Rate Of Change Values
def calculateROC(stockDF):
  rocList = [1 for i in range (14)]

  for x in range(14, len(stockDF.index+1)):
    rocList.append(((stockDF.at[x, "close"] -  stockDF.at[x-14, "close"])/  stockDF.at[x-14, "close"]) * 100)

  stockDF.insert(9, "ROC", rocList, True)

  return stockDF


def calculateEMA(stockDF, periods):
  weighting =  (2 / (periods + 1) ) 
  
  emaList = [1 for x in range(periods)]

  initSmlMovingAverage = 0.0

  #Small moving average calculatiion
  for x in range(periods):
    initSmlMovingAverage += stockDF.at[x, "close"]

  initSmlMovingAverage = initSmlMovingAverage / periods

  for x in range(periods, len(stockDF.index+1)):
    if(x==0):
      emaList.append(   (stockDF.at[x, "close"] * weighting) +  initSmlMovingAverage*(1-weighting)  )
    else:
       emaList.append(   (stockDF.at[x, "close"] * weighting) +  emaList[x-1]*(1-weighting)  )

  stockDF.insert(len(stockDF.columns), "EMA "+str(periods), emaList, True)

  return stockDF


def calculateMACD(stockDF):
  macdList = [1 for i in range(26)]  

  for x in range(26, len(stockDF.index+1)):
    macdList.append(stockDF.at[x, "EMA 12"]-stockDF.at[x, "EMA 26"])

  stockDF.insert(len(stockDF.columns),"MACD", macdList ,True)

  return stockDF

def calculateTypicalPrice(stockDF):
  typList = []

  for x in range(len(stockDF.index +1)):
    typList.append((stockDF.at[x, "high"] + stockDF.at[x, "low"] + stockDF.at[x, "close"]) /3)
  
  stockDF.insert(len(stockDF.columns),"Typical Price", typList ,True)

  return stockDF

def calculateRawMoneyFlow(stockDF):
  rawMoneyFlowList = []

  for x in range(len(stockDF.index +1)):
    rawMoneyFlowList.append(stockDF.at[x, "Typical Price"] * stockDF.at[x, "volume"])

  stockDF.insert(len(stockDF.columns),"Raw Money Flow", rawMoneyFlowList ,True)

  return stockDF

def calculateMoneyFlowIndex(stockDF):
  
  mfiList = [1 for x in range(15)]
  

  for x in range(15, len(stockDF.index + 1)):
    posMoneyFlow = 0
    negMoneyFlow = 0
    
    for i in range(x-14, x):
      if((stockDF.at[i, "Raw Money Flow"] - stockDF.at[i-1, "Raw Money Flow"]) > 0):
        posMoneyFlow += stockDF.at[i, "Raw Money Flow"]
      elif((stockDF.at[i, "Raw Money Flow"] - stockDF.at[i-1, "Raw Money Flow"]) < 0):
        negMoneyFlow += stockDF.at[i, "Raw Money Flow"]

    mfiList.append(100 - ( 100/ (1+ (posMoneyFlow/negMoneyFlow) ) ) )
  
  stockDF.insert(len(stockDF.columns),"Money Flow Index", mfiList ,True)

  return stockDF


# Shifts the close price so the model trains off the future values

def shiftClosePriceForFuture(stockDF, periodsToPredict):
  closeList = stockDF["close"].tolist()

  for x in range(periodsToPredict):
    closeList.insert(0, 0)
  
  for x in range(periodsToPredict):
    closeList.pop(len(closeList)-1)

  stockDF.drop("close", axis = 1, inplace = True)

  stockDF.insert(0,"Future Close", closeList ,True)

  return stockDF

def fixStockDataFrame(stockDF):
  stockDF.drop([i for i in range(26)], 0, inplace = True) 

  stockDF = stockDF[["Future Close", "RSI", "ROC", "MACD", "Money Flow Index"]]
  
  return stockDF





  