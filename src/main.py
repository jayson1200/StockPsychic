import pickle
import StockInfoGetter
import pandas as pd
import sklearn
from sklearn import linear_model
import numpy as np

import stockmodel
from stockmodel import Stockmodel

def main():
    print("\n You probably want to avoid minute because it has a lot periods where zero change happens, which might result in a division by 0 \n")

    usrResponse = str(input("Do you want to make a model with our test URL: Test\nMake a model with your own characteristics defined in the URL for the HTTPRequest: New\nOr use a model already defined: Run\n"))

    if(usrResponse == "Test"):
        runTest()

    elif(usrResponse == "New"):
        jdModel = Stockmodel("jdmodel")

        jdModel.printDataFrame()

        jdModel.updateModel()

        jdModel.printAccuracy()

        print("The predicted price is %s" % jdModel.predict(100, 70, 3.00, 2.01, 90.01))


    elif(usrResponse == "Run"):
        pass
        

if __name__ == "__main__":
    main()





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
    