from strategies.botstrategy import BotStrategy
from botposition import BotPosition

class SRsi(BotStrategy):
    def __init__(self):
        super(SRsi,self).__init__()
        self.derivee = 0
        self.RSI_data = []
        self.RSI_moyenne = []
        self.last_average = 0.

    def open_position(self,candlestick):
        res = False
        self.RSI_data.append(self.indicators.RSI(self.prices,14))
        self.RSI_moyenne.append(self.indicators.exp_moyenne(self.RSI_data,12,self.last_average))
        self.lastAverage = self.RSI_moyenne[-1]
        if len(self.RSI_moyenne) == 1:
            deriv = 0
        else:
            deriv = (self.RSI_moyenne[-1]-self.RSI_moyenne[-2])
        if self.derivee <=0 and deriv>0. and len(self.RSI_moyenne) > 14:
            res = True
        self.derivee = deriv
        if res:
            return BotPosition(self.current_price,candlestick.start_time,short = False)
        else:
            return None


    def try_close_position(self,position,candlestick):
        res = False
        self.RSI_data.append(self.indicators.RSI(self.prices,14))
        self.RSI_moyenne.append(self.indicators.exp_moyenne(self.RSI_data,12,self.last_average))
        self.last_average = self.RSI_moyenne[-1]
        if len(self.RSI_moyenne) == 1:
            deriv = 0
        else:
            deriv = (self.RSI_moyenne[-1]-self.RSI_moyenne[-2])
        if self.derivee >=0 and deriv<-0. and len(self.RSI_moyenne) > 14:
            res = True
        self.derivee = deriv
        if res:
            position.close(self.current_price,candlestick.start_time)
