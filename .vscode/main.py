import StockInfoGetter



def main():
    apiKey = input("Can I have your TD Ameritrade API key")
    ticker= input("Can I have the ticker symbol that you want")

    StockInfoGetter.getStockInfo(ticker, apiKey)


if __name__ == "__main__":
    main()
