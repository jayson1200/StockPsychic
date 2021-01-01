

class TrailStopManager:
    
    def __init__(self, salePrice, stopLossPercent, trailStopLossPercent):
        self.salePrice = salePrice
        self.stopLossPercent = stopLossPercent
        self.trailStopLossPercent = trailStopLossPercent
        self.highestPrice = salePrice
    
    
    def shouldSell(self, currentPrice):
        
        if self.highestPrice < currentPrice:
            self.highestPrice = currentPrice

        if ((currentPrice - self.salePrice)/self.salePrice) >= self.stopLossPercent:
            if ((currentPrice - self.highestPrice)/ self.highestPrice) <= -self.trailStopLossPercent:
                return True
            else:
                return False
        elif ((currentPrice - self.salePrice)/self.salePrice) < -self.stopLossPercent:
            return True
        
        return False   
