import StockInfoGetter

def main():
    
    
    params = {"apiKey": input("Can I have your TD Ameritrade API key"), "ticker" : input("Can I have the ticker symbol that you want"), "periodType" : None, "period" : None, "frequencyType" : None}
    #period = input("What Day, month, year, or ")

    StockInfoGetter.getStockInfo(apiKey=params["apiKey"], ticker= params["ticker"])


if __name__ == "__main__":
    main()
