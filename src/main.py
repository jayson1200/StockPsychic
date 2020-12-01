import pickle
import StockInfoGetter
import pandas as pd
import sklearn
from sklearn import linear_model
import numpy as np

def main():
    print("\n You probably want to avoid minute because it has a lot periods where zero change happens, which might result in a division by 0 \n")

    usrResponse = str(input("Do you want to make a model with our test URL: Test\nMake a model with your own characteristics defined in the URL for the HTTPRequest: New\nOr use a model already defined: Run\n"))

    if(usrResponse == "Test"):
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
        x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.1)

        for x in range(1000000):
            x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.1)

            stockModel = linear_model.LinearRegression()

            stockModel.fit(x_train, y_train)

            acc = stockModel.score(x_test, y_test)
            
            if(acc > currentHighestAcc):
                print("Accuracy: %f" % acc)
                currentHighestAcc = acc
                with open("stockmodel.pickle", "wb") as f:
                    pickle.dump(stockModel, f)

    elif(usrResponse == "New"):
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
    
        X = np.array(stockInfoDF.drop("Future Close", axis = 1))
        y = np.array(stockInfoDF["Future Close"])

        

        currentHighestAcc = 0
        x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.1)

        for x in range(10):
            x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.1)

            stockModel = linear_model.LinearRegression()

            stockModel.fit(x_train, y_train)

            acc = stockModel.score(x_test, y_test)
            
            if(acc > currentHighestAcc):
                print("Accuracy: %f" % acc)
                currentHighestAcc = acc
                with open("stockmodel.pickle", "wb") as f:
                    pickle.dump(stockModel, f)

    elif(usrResponse == "Run"):
        modelFileName = input("\nWhat is the file name ")

        arrayOfVals = [] 
    
        arrayOfVals.append(float(input("Close Value: ")))
        arrayOfVals.append(float(input("RSI Value: ")))
        arrayOfVals.append(float(input("ROC Value: ")))
        arrayOfVals.append(float(input("MACD: ")))
        arrayOfVals.append(float(input("Money Flow Index: ")))

        print(arrayOfVals)

        pickleVal = open(modelFileName, "rb")
        stockModel = pickle.load(pickleVal)

        print("\nThe estimated price is %f" %  stockModel.predict([arrayOfVals, arrayOfVals])[0] )
        

if __name__ == "__main__":
    main()
