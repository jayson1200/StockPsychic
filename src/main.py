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
        "frequencyType" : "weekly"
        } 
    else:
        params = {
        "apiKey": input("Can I have your TD Ameritrade API key "), 
        "ticker" : input("Can I have the ticker symbol that you want "), 
        "periodType" : input("What type of period: day, month, or year "), 
        "period" : input("How many periods "), 
        "frequencyType" : input("In what frequency: minute, daily, weekly, or monthly ")
        }
    
    
    stockInfoDF = StockInfoGetter.getStockInfo(apiKey=params["apiKey"], ticker= params["ticker"], periodType = params["periodType"], period = params["period"], frequencyType = params["frequencyType"])
    stockInfoDF = StockInfoGetter.calculateRSIData(stockInfoDF)

if __name__ == "__main__":
    main()
