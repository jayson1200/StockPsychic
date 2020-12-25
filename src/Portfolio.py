
class Portfolio:
    
    def __init__(self, amtMoney):
        self.amtMoney = amtMoney
        self.positions = {}


    def makePosition(self, ticker, sharePrice, **kwargs):
        
        if kwargs.get("runSugStrat") == True:
            amtOfShares = int((self.amtMonet/2) / sharePrice)
        else:
            amtOfShares = kwargs.get("sharesToBuy")

        self.amtMoney -= self.amtOfShares * sharePrice

        self.positions[ticker] = amtOfShares


    def closePosition(self, ticker, sharePrice):

        self.amtMoney += sharePrice * self.positions[ticker]

        del self.positions[ticker]


    def getAmtMoney(self):
        return self.amtMoney

        
