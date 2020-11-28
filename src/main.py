import StockInfoGetter
import pandas as pd

def main():
    print("\n You probably want to avoid minute because it has a lot periods where zero change happens, which might result in a division by 0 \n")

    if(str(input("Do you want to run a test ")) == ("yes" or "Yes")):
        params = {
        "apiKey": "I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF",
        "ticker" : "AAPL",
        "periodType" : "year",
        "period" : 20,
        "frequencyType" : "weekly",
        "futureOffset" : 1
        } 
    else:
        params = {
        "apiKey": input("Can I have your TD Ameritrade API key "), 
        "ticker" : input("Can I have the ticker symbol that you want "), 
        "periodType" : input("What type of period: day, month, or year "), 
        "period" : input("How many periods "), 
        "frequencyType" : input("In what frequency: minute, daily, weekly, or monthly "),

        # I need to train the model based on how far the user wants to predict
        "futureOffset" : int(input("How many periods into the future do you want to predict "))
        }
    
    
    stockInfoDF = StockInfoGetter.getStockInfo(apiKey=params["apiKey"], ticker= params["ticker"], periodType = params["periodType"], period = params["period"], frequencyType = params["frequencyType"])
    stockInfoDF = StockInfoGetter.calculateRSIData(stockInfoDF)
    stockInfoDF = StockInfoGetter.calculateROC(stockInfoDF)
    stockInfoDF = StockInfoGetter.calculateEMA(stockInfoDF, 26)
    stockInfoDF = StockInfoGetter.calculateEMA(stockInfoDF, 12)
    stockInfoDF = StockInfoGetter.calculateMACD(stockInfoDF)
    stockInfoDF = StockInfoGetter.calculateTypicalPrice(stockInfoDF)
    stockInfoDF = StockInfoGetter.calculateRawMoneyFlow(stockInfoDF)
    stockInfoDF = StockInfoGetter.calculateMoneyFlowIndex(stockInfoDF)
    stockInfoDF = StockInfoGetter.shiftClosePriceForFuture(stockInfoDF, params["futureOffset"]) 
    stockInfoDF = StockInfoGetter.fixStockDataFrame(stockInfoDF)
   

    print(stockInfoDF)










if __name__ == "__main__":
    main()
