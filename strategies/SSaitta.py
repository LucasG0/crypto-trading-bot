from strategies.botstrategy import BotStrategy
from botposition import BotPosition

# Strategy based on Saitta indicator.
class SSaitta(BotStrategy):
    def __init__(self):
        super(SSaitta,self).__init__()

    def open_position(self,candlestick):
        resistance = self.indicators.saitta_support_resistance(self.high,self.low,12)[1]
        temp = self.current_price > resistance
        if temp:
            return BotPosition(self.current_price,candlestick.start_time,short = False)
        else:
            return None

    def try_close_position(self,position,candlestick):
        support = self.indicators.saitta_support_resistance(self.high,self.low,12)[0]
        temp = self.current_price < support
        if temp:
            position.close(self.current_price,candlestick.start_time)
