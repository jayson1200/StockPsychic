import StockInfoGetter

def main():
    
    if(input("Do you want to run a test") == "Yes" or "yes"):
        params = {
        "apiKey": "I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF",
        "ticker" : "AAPL",
        "periodType" : "day",
        "period" : 10,
        "frequencyType" : "minute"
        } 
    else:
        params = {
        "apiKey": input("Can I have your TD Ameritrade API key"), 
        "ticker" : input("Can I have the ticker symbol that you want"), 
        "periodType" : input("What type of period: day, month, or year"), 
        "period" : input("How many periods"), 
        "frequencyType" : input("In what frequency: minute, daily, weekly, or monthly")
        }
    
    
    StockInfoGetter.getStockInfo(apiKey=params["apiKey"], ticker= params["ticker"], periodType = params["periodType"], period = params["period"], frequencyType = params["frequencyType"])


if __name__ == "__main__":
    main()
