class StockObject():
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.predictedChange = -100000000000.0

    def setPredictedChange(self, percentChange):
        self.predictedChange = percentChange

    
    def getTicker(self):
        return self.ticker

    def getPredictedChange(self):
        return self.predictedChange

    def clearPredictedChange(self):
        self.predictedChange = -100000000000.0