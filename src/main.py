import pickle
import StockInfoGetter
import pandas as pd
import sklearn
from sklearn import linear_model
import numpy as np
from stockmodel import Stockmodel
from StockObj import StockObject
import requests
from requests.models import HTTPError
import time

def main():
    intradayTrading()
    # print("\n You probably want to avoid minute because it has a lot periods where zero change happens, which might result in a division by 0 \n")

    # usrResponse = str(input("Do you want to make a model with our test URL: Test\nMake a model with your own characteristics defined in the URL for the HTTPRequest: New\nOr use a model already defined: Run\n"))
    
    # jdModel = Stockmodel("jdmodel")

    # if(usrResponse == "Test"):
    #     runTest()

    # elif(usrResponse == "New"):
    #     jdModel = Stockmodel("jdmodel")

    #     jdModel.printDataFrame()
        
    #     jdModel.printAccuracy()


    # elif(usrResponse == "Run"):
    #     print("The predicted price is %s" % jdModel.predict(100, 70, 3.00, 2.01, 90.01))
    

    """
    Have two strategies one that makes intraday trades and one that trys to make day and week trades 
    Each strategy will have there own pool of money
    """

    """
    Have a while loop that runs forever, 
    and one within that will pause the while loop when we're not in market hours
    
    Make a stockmodel on a bunch of leveraged etfs  
    Check the prediction for the stockmodel 
    The one that beats a certain threshold is picked
    If there are no positive predictions I will wait a certain amount of time and try again

    Once I find one I keep on checking the price evey few minutes or hours depending on which strategy and see if it has reached the threshold of acceptable profit or acceptable loss
    After that I go back to my list of leveraged etfs and repeat

    Print how much money was made and the current balance on every sell
    """   

"""securitiesToLookAt = [StockObject("SPXU"), StockObject("SQQQ"), StockObject("SDOW"), StockObject("UPRO"), StockObject("TQQQ"), 
                          StockObject("UDOW"), StockObject("DFEN"), StockObject("WEBS"), StockObject("FAZ"), StockObject("WANT"),
                          StockObject("UGLD"), StockObject("DGLD"), StockObject("USLV"), StockObject("DSLV"), StockObject("UGAZ"),  
                          StockObject("WEBL"), StockObject("FAS"), StockObject("CURE"), StockObject("NAIL"), StockObject("DUSL"),
                          StockObject("DRV"), StockObject("DRN"), StockObject("PILL"), StockObject("DPST"), StockObject("RETL"),
                          StockObject("HIBS"), StockObject("HIBL"), StockObject("LABD"), StockObject("LABU"), StockObject("SOXS"),
                          StockObject("SOXL"), StockObject("TECS"), StockObject("TECL"), StockObject("TPOR"), StockObject("UTSL")]"""

def intradayTrading():
    
    securitiesToLookAt = [StockObject("SQQQ"), StockObject("UPRO"), StockObject("TQQQ"), 
                          StockObject("WEBS"), StockObject("UGAZ"), StockObject("WEBL"), 
                          StockObject("CURE"), StockObject("HIBS"), StockObject("HIBL"),
                          StockObject("TECS"), StockObject("TECL")]

    intradayTradingParams = { 
        "periodType" : "day", 
        "period" : 10, 
        "frequencyType" : "minute",
        "futureOffset" : 360 # 6 hours
    }

    tdApiKey = "I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF"
    advApiKey = "OH4XYOJUKWRL7ERG"

    amountOfMoney = 2000

    runOnce = True
    # I need to decide how many shares to buy and I also need to add a trailing stop loss
    while(runOnce):


        # Makes a model for the ticker symbol in each of the objects in the securitiesToLookAt list and assigns a predicted value inside each StockObject
        for i in range(len(securitiesToLookAt)):
            
            objModel = Stockmodel(tdApiKey, securitiesToLookAt[i].getTicker(), intradayTradingParams["periodType"], intradayTradingParams["period"], 
            intradayTradingParams["frequencyType"], intradayTradingParams["futureOffset"], securitiesToLookAt[i].getTicker())

            close = 0.0
            rsi = 0.0
            roc = 0.0
            macd = 0.0
            mfi = 0.0

            closeUrl = "https://api.tdameritrade.com/v1/marketdata/"+ securitiesToLookAt[i].getTicker() +"/quotes?apikey="+tdApiKey
            rsiUrl = "https://www.alphavantage.co/query?function=RSI&symbol="+ securitiesToLookAt[i].getTicker() + "&interval=1min&time_period=14&series_type=close&apikey=" + advApiKey
            rocUrl = "https://www.alphavantage.co/query?function=ROC&symbol="+ securitiesToLookAt[i].getTicker() + "&interval=1min&time_period=14&series_type=close&apikey=" + advApiKey
            macdUrl = "https://www.alphavantage.co/query?function=MACD&symbol="+ securitiesToLookAt[i].getTicker() + "&interval=1min&time_period=14&series_type=close&apikey=" + advApiKey
            mfiUrl = "https://www.alphavantage.co/query?function=MFI&symbol="+ securitiesToLookAt[i].getTicker() + "&interval=1min&time_period=14&series_type=close&apikey=" + advApiKey

            try:
                close = requests.get(closeUrl).json()[securitiesToLookAt[i].getTicker()]["closePrice"]

                rsiDictVals = requests.get(rsiUrl).json()["Technical Analysis: RSI"]
                rsi = rsiDictVals[rsiDictVals.keys()[0]]["RSI"]

                rocDictVals = requests.get(rocUrl).json()["Technical Analysis: ROC"]
                roc = rocDictVals[rocDictVals.keys()[0]]["ROC"]

                macdDictVals = requests.get(macdUrl).json()["Technical Analysis: MACD"]
                macd = macdDictVals[macdDictVals.keys()[0]]["MACD"]

                mfiDictVals = requests.get(mfiUrl).json()["Technical Analysis: MFI"]
                mfi = mfiDictVals[mfiDictVals.keys()[0]]["MFI"]

            except HTTPError:
                print("We don't have your info")
            except Exception:
                print("Something Happened")
    
            securitiesToLookAt[i].setPredictedChange(     (objModel.predict(close, rsi, roc, macd, mfi) - close)/close   )   

            time.sleep(60000)

        bestStockModel = StockObject("L")

        # Loops through all of the stocks to see which one has the best upside potential
        for i in range(len(securitiesToLookAt)):
            if bestStockModel.getPredictedChange() < securitiesToLookAt[i].getPredictedChange:
                bestStockModel = securitiesToLookAt[i]


        saleClose = 0
        holdingStock = False
        
        # If the best prediction gives a profit of 2% it will buy the stock
        # Else it will stop the loop and start making new stock models
        if(bestStockModel.getPredictedChange() >= 0.02):
            
            holdingStock = True

            closeUrl = "https://api.tdameritrade.com/v1/marketdata/"+ bestStockModel.getTicker() +"/quotes?apikey="+tdApiKey

            try:
                saleClose = requests.get(closeUrl).json()[bestStockModel.getTicker()]["closePrice"]
            except HTTPError:
                print("We don't have your info")
            except Exception:
                print("Something Happened")

            amountOfMoney -= saleClose
        else:
            continue
        
        # Waits for the optimal oppurtunity to sell 
        while holdingStock:
            time.sleep(300000)

            currentClose = 0

            closeUrl = "https://api.tdameritrade.com/v1/marketdata/"+ bestStockModel.getTicker() +"/quotes?apikey="+tdApiKey

            try:
                currentClose = requests.get(closeUrl).json()[bestStockModel.getTicker()]["closePrice"]
            except HTTPError:
                print("We don't have your info")
            except Exception:
                print("Something Happened")

            amountOfMoney -= saleClose
            
            percentChange = ((currentClose - saleClose) / saleClose)

            if (percentChange >= 0.02) or (percentChange <= 0.03):
                amountOfMoney += currentClose
                holdingStock = False

        print(amountOfMoney)
        runOnce = False
            






def runTest():

    params = {
        "apiKey": "I4WJTVFRTTZ7AUWEGIKYMPSKSUPXAKCF",
        "ticker" : "AAPL",
        "periodType" : "year",
        "period" : 20,
        "frequencyType" : "daily",
        "futureOffset" : 1
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

    X = np.array(stockInfoDF.drop("Future Close", axis = 1))
    y = np.array(stockInfoDF["Future Close"])

    currentHighestAcc = 0
    x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

    for x in range(10):
        x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

        stockModel = linear_model.LinearRegression()

        stockModel.fit(x_train, y_train)

        acc = stockModel.score(x_test, y_test)
        
        if(acc > currentHighestAcc):
            print("Accuracy: %f" % acc)
            currentHighestAcc = acc
            with open("stockmodel.pickle", "wb") as f:
                pickle.dump(stockModel, f)


if __name__ == "__main__":
    main()
    