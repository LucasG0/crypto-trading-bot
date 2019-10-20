from strategies.botstrategy import BotStrategy
from botposition import BotPosition

# Strategy based on stochastic indicator with a 1mn period.
# Exponential average and pivot are used in order to detect the trend (price behavior on a longer period).
class SStochastique(BotStrategy):
    def __init__(self, chart_m5, chart_m15, chart_d1):
        super(SStochastique,self).__init__()
        self.stop_loss = 0.001
        self.data_m5 = init_chart(chart_m5)
        self.data_m15 = init_chart(chart_m15)
        self.data_d1 = init_chart(chart_d1)
        self.inf_20 = False
        self.mean_timming = [0,0,0,0]
        self.mean_m5 = [0,0,0,0]
        self.mean_m15 = [0,0,0,0]

    def buy_priority(self,candlestick):
        p = self.current_price
        self.mean_timming[0] = self.indicators.exp_average(self.prices,candlestick,100,self.mean_timming[0])
        self.mean_timming[1] = self.indicators.exp_average(self.prices,candlestick,300,self.meanTimming[1])
        self.mean_timming[2] = self.indicators.exp_average(self.prices,candlestick,600,self.mean_timming[2])
        self.mean_timming[3] = self.indicators.exp_average(self.prices,candlestick,1000,self.mean_timming[3])
        sens_m1 = p > self.mean_timming[0] and p > self.mean_timming[1] and p > self.mean_timming[2] and p > self.mean_timming[3]
        self.mean_m5[0] = self.indicators.exp_average(self.data_m5[0],candlestick,100,self.mean_m5[0])
        self.mean_m5[1] = self.indicators.exp_average(self.data_m5[0],candlestick,300,self.mean_m5[1])
        self.mean_m5[2] = self.indicators.exp_average(self.data_m5[0],candlestick,600,self.mean_m5[2])
        self.mean_m5[3] = self.indicators.exp_average(self.data_m5[0],candlestick,1000,self.mean_m5[3])
        sensM5 = p > self.meanM5[0] and p > self.meanM5[1] and p > self.meanM5[2] and p > self.meanM5[3]
        self.mean_m15[0] = self.indicators.exp_average(self.data_m15[0],candlestick,100,self.mean_m15[0])
        self.mean_m15[1] = self.indicators.exp_average(self.data_m15[0],candlestick,300,self.mean_m15[1])
        self.mean_m15[2] = self.indicators.exp_average(self.data_m15[0],candlestick,600,self.mean_m15[2])
        self.mean_m15[3] = self.indicators.exp_average(self.data_m15[0],candlestick,1000,self.mean_m15[3])
        sens_m15 = p > self.mean_m15[0] and p > self.mean_m15[1] and p > self.mean_m15[2] and p > self.mean_m15[3]
        pivot_d1 = (self.data_d1[0][-1] + self.data_d1[1][-1] + self.data_d1[2][-1])/float(3)
        sens_pivot = p > pivot_d1
        return sens_m1 and sens_m5 and sens_m15 and sens_pivot

    def cond_stochastique(self,candlestick):
        stochastique = self.indicators.stochastique(self.prices,self.low,self.high,14)
        if (stochastique < 20):
            self.inf20 = True
            return False
        else:
            if(self.inf20):
                self.inf20 = False
                if self.buy_priority(candlestick):
                    return True
            else:
                self.inf20 = False
                return False

    def open_position(self,candlestick):
        st = self.cond_stochastique(candlestick)
        prio = self.buy_priority(candlestick)
        temp = prio and st
        if temp:
            return BotPosition(self.current_price,candlestick.start_time,short = False)
        else:
            return None

    def try_close_position(self,position,candlestick):
        temp = self.current_price - trade.entry_price > self.stop_loss
        if temp:
            position.close(self.current_price,candlestick.start_time)

def init_chart(chart):
    prices = []
    high = []
    low = []
    for candlestick in chart.getPoints():
        prices.append(candlestick.close)
        high.append(candlestick.high)
        low.append(candlestick.low)
    return [prices,low,high];
