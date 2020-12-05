import pickle

from pandas.core.frame import DataFrame
import StockInfoGetter
import pandas as pd
import sklearn
from sklearn import linear_model
import numpy as np

class Stockmodel:

    """Used to make and run the model"""

    # Asks the user for the initial paramters. Gets the information based on those parameters and trains the model
    def __init__(self, modelFileName):

        self.modelFileName = modelFileName
        self.stockInfoDF = DataFrame()
        self.acc = 0


        self.params = {
        "apiKey": input("Can I have your TD Ameritrade API key "), 
        "ticker" : input("Can I have the ticker symbol that you want "), 
        "periodType" : input("What type of period: day, month, or year "), 
        "period" : input("How many periods "), 
        "frequencyType" : input("In what frequency: minute, daily, weekly, or monthly "),

        # I train the model based on how far the user wants to predict
        "futureOffset" : int(input("How many periods into the future do you want to predict "))
        }

        self.stockInfoDF = StockInfoGetter.getStockInfo(apiKey=self.params["apiKey"], ticker= self.params["ticker"], periodType = self.params["periodType"], period = self.params["period"], frequencyType = self.params["frequencyType"])
        self.stockInfoDF = StockInfoGetter.calculateRSIData(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateROC(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateEMA(self.stockInfoDF, 26)
        self.stockInfoDF = StockInfoGetter.calculateEMA(self.stockInfoDF, 12)
        self.stockInfoDF = StockInfoGetter.calculateMACD(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateTypicalPrice(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateRawMoneyFlow(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateMoneyFlowIndex(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.shiftClosePriceForFuture(self.stockInfoDF, self.params["futureOffset"]) 
        self.stockInfoDF = StockInfoGetter.fixStockDataFrame(self.stockInfoDF)
    
        X = np.array(self.stockInfoDF.drop("Future Close", axis = 1))
        y = np.array(self.stockInfoDF["Future Close"])

        

        currentHighestAcc = 0
        x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

        for x in range(10):
            x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

            stockModel = linear_model.LinearRegression()

            stockModel.fit(x_train, y_train)

            self.acc = stockModel.score(x_test, y_test)
            
            if(self.acc > currentHighestAcc):
                currentHighestAcc = self.acc
                with open(str(self.modelFileName + ".pickle"), "wb") as f:
                    pickle.dump(stockModel, f)

   
    
    # Updates and retrains the model based on new data that might have changed
    def updateModel(self):
        self.acc = 0
        self.stockInfoDF = StockInfoGetter.getStockInfo(apiKey=self.params["apiKey"], ticker= self.params["ticker"], periodType = self.params["periodType"], period = self.params["period"], frequencyType = self.params["frequencyType"])
        self.stockInfoDF = StockInfoGetter.calculateRSIData(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateROC(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateEMA(self.stockInfoDF, 26)
        self.stockInfoDF = StockInfoGetter.calculateEMA(self.stockInfoDF, 12)
        self.stockInfoDF = StockInfoGetter.calculateMACD(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateTypicalPrice(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateRawMoneyFlow(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.calculateMoneyFlowIndex(self.stockInfoDF)
        self.stockInfoDF = StockInfoGetter.shiftClosePriceForFuture(self.stockInfoDF, self.params["futureOffset"]) 
        self.stockInfoDF = StockInfoGetter.fixStockDataFrame(self.stockInfoDF)
    
        X = np.array(self.stockInfoDF.drop("Future Close", axis = 1))
        y = np.array(self.stockInfoDF["Future Close"])

        

        currentHighestAcc = 0
        x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

        for x in range(10):
            x_train, x_test,  y_train,  y_test = sklearn.model_selection.train_test_split(X, y, test_size  = 0.2)

            stockModel = linear_model.LinearRegression()

            stockModel.fit(x_train, y_train)

            self.acc = stockModel.score(x_test, y_test)
            
            if(self.acc > currentHighestAcc):
                currentHighestAcc = self.acc
                with open(str(self.modelFileName + ".pickle"), "wb") as f:
                    pickle.dump(stockModel, f)

    # Prints information on the model
    def printModelInfo(self):
        print("Model Characteristics:")
        for key, value in self.params.items():
            print(key, ' -> ', value)

    # Returns a peridicted price based on the given parameters
    def predict(self, close, rsi, roc, macd, mfi):
        pickleVal = open(str(self.modelFileName + ".pickle"), "rb")
        stockModel = pickle.load(pickleVal)

        arrayOfVals = [close, rsi, roc, macd, mfi]

        return stockModel.predict([arrayOfVals, arrayOfVals])[0]

    # Prints the dataframe
    def printDataFrame(self):
        print(self.stockInfoDF)

    def printAccuracy(self):
        print("The model's self.accuracy is %s" %  self.acc)