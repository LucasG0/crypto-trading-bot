import plotly
from botchart import BotChart
import timetranslate as tt
from strategies.botstrategy import BotStrategy

# Allows to plot a graph with candlesticks, indicators and portfolio.
class PlotGraphe(object):
    def __init__(self,chart,strategy):
        self.chart = chart
        self.strategy = strategy
        self.perf = []


    def plotRsi(self,prices,temps):

        RSI_data = []
        RSI_moyenne = []
        lastAverage = 0.
        for i in range(1,len(prices)):
            RSI_data.append(self.strategy.indicators.RSI(prices[:i],14))
            RSI_moyenne.append(self.strategy.indicators.simple_average(RSI_data[:i],12))
            # RSI_moyenne.append(self.strategy.indicators.expMoyenne(RSI_data[:i],21,lastAverage))
            lastAverage = RSI_moyenne[-1]
        # RSI_data.append(50)



        rsi = plotly.graph_objs.Scatter(
        x = temps,
        y = RSI_data,
        marker = dict(size = 10,color = 'rgba(255, 0, 255, .9)')
        )

        rsi_moy = plotly.graph_objs.Scatter(
        x = temps,
        y = RSI_moyenne,
        # y = [30 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(0, 0, 0, .9)')
        )

        rsi_min = plotly.graph_objs.Scatter(
        x = temps,
        y = [30 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        rsi_max = plotly.graph_objs.Scatter(
        x = temps,
        y = [70 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        return rsi,rsi_moy,rsi_min,rsi_max

    def plotStochastique(self,prices,low,high,temps):

        STOCH_data = []
        for i in range(1,len(prices)):
            STOCH_data.append(self.strategy.indicators.stochastique(prices[:i],low[:i],high[:i],14));
        # STOCH_data.append(50)

        stoch = plotly.graph_objs.Scatter(
        x = temps,
        y = STOCH_data,
        marker = dict(size = 10,color = 'rgba(255, 0, 255, .9)')
        )

        stoch_min = plotly.graph_objs.Scatter(
        x = temps,
        y = [20 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        stoch_max = plotly.graph_objs.Scatter(
        x = temps,
        y = [80 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        return stoch,stoch_min,stoch_max

    def plotBollinger(self,prices,temps):
        bollSup_data = [prices[0]]
        boll_data = [prices[0]]
        bollInf_data = [prices[0]]
        for i in range(1,len(prices)):
            bollSup_data.append(self.strategy.indicators.bollinger(prices[:i])[2])
            boll_data.append(self.strategy.indicators.bollinger(prices[:i])[1])
            bollInf_data.append(self.strategy.indicators.bollinger(prices[:i])[0])

        bollSup = plotly.graph_objs.Scatter(
        x = temps,
        y = bollSup_data,
        marker = dict(color= 'rgba(0,255,50,0.7)')
        )

        boll = plotly.graph_objs.Scatter(
        x = temps,
        y = boll_data,
        fill='tonexty',
        fillcolor = 'rgba(0,255,50,0.05)',
        marker = dict(color= 'rgba(0,255,50,0.7)')
        )
        bollInf = plotly.graph_objs.Scatter(
        x = temps,
        y = bollInf_data,
        fill='tonexty',
        fillcolor = 'rgba(0,255,50,0.05)',
        marker = dict(color= 'rgba(0,255,50,0.7)')
        )
        return bollSup,boll,bollInf

    def plotIchimoku(self,high,low,tempsA,tempsB):
        senkou_span_A_data =[]
        senkou_span_B_data =[]
        for i in range(1,len(high)):
            senkou_span_A_data.append(self.strategy.indicators.ichimoku(high[:i],low[:i])[0])
            senkou_span_B_data.append(self.strategy.indicators.ichimoku(high[:i],low[:i])[1])

        span_A = plotly.graph_objs.Scatter(
        x = tempsA,
        y = senkou_span_A_data,
        marker = dict(color= 'rgb(0,0,250)')
        )

        span_B = plotly.graph_objs.Scatter(
        x = tempsB,
        y = senkou_span_B_data,
        fill='tonexty',
        fillcolor = 'rgba(150,0,155,0.1)',
        marker = dict(color= 'rgb(255,0,0)')
        )
        return span_A,span_B

    def plotLongPosition(self,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time):

        trade_entry_data = [t * 1 for t in trade_entry_data]
        trade_exit_data = [t * 1 for t in trade_exit_data]
        entryPoint = plotly.graph_objs.Scatter(
        x = trade_entry_time,
        y = trade_entry_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(0, 255, 0, .9)')
        )

        exitPoint = plotly.graph_objs.Scatter(
        x = trade_exit_time,
        y = trade_exit_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        return entryPoint,exitPoint

    def plotShortPosition(self,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time):

        trade_entry_data = [t * 1 for t in trade_entry_data]
        trade_exit_data = [t * 1 for t in trade_exit_data]
        entryPoint = plotly.graph_objs.Scatter(
        x = trade_entry_time,
        y = trade_entry_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(0, 0, 255, .9)')
        )

        exitPoint = plotly.graph_objs.Scatter(
        x = trade_exit_time,
        y = trade_exit_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(120, 120, 0, .9)')
        )

        return entryPoint,exitPoint

    def plotPortfolio(self,close_data,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time,temps):
        unit = [1.]
        try:
            portfolioValue = [trade_entry_data[0]]
            j = 0
            L = len(trade_exit_time)
            trade_open = False
            for i in range(len(temps)):
                if L>j:
                    if trade_open == False:
                        if temps[i] == trade_entry_time[j]:
                            trade_open = True
                            unit.append(portfolioValue[-1]/trade_entry_data[j])
                            portfolioValue.append(unit[-1]*close_data[i])
                        else:
                            portfolioValue.append(portfolioValue[-1])
                            unit.append(portfolioValue[-1]/close_data[i])
                    else:
                        if temps[i] == trade_exit_time[j]:
                            trade_open = False
                            portfolioValue.append(unit[-1]*trade_exit_data[j])
                            unit.append(unit[-1])
                            j += 1
                        else :
                            portfolioValue.append(unit[-1]*close_data[i])
                            unit.append(unit[-1])
                else:
                    portfolioValue.append(portfolioValue[-1])
                    unit.append(unit[-1])

            self.perf = (portfolioValue[-1]-portfolioValue[0])/portfolioValue[0]*100

        except Exception as e:
            self.perf = 1
            self.unit = [1]
            portfolioValue = [0]

        portfolio = plotly.graph_objs.Scatter(
        x = temps,
        y = portfolioValue,
        mode = 'lines+markets',
        marker = dict(size = 10,color = 'rgba(0, 0, 255, .9)')
        )
        perf = plotly.graph_objs.Scatter(
        x = temps,
        y = unit,
        yaxis = 'y2',
        mode = 'lines+markets',
        marker = dict(size = 10,color = 'rgba(0, 0, 0, .9)')
        )

        return [portfolio,perf]

    def plotCandle(self,open_data,close_data,high_data,low_data,x_data):

        trace = plotly.graph_objs.Candlestick(
            x = x_data,
            open = open_data,
            close = close_data,
            high = high_data,
            low = low_data)
        return trace

    def plotChart(self):

        open_data = []
        close_data = []
        high_data = []
        low_data = []
        x_data = []
        x_data_ichimokuA =[]
        x_data_ichimokuB =[]
        long_entry_data = []
        long_entry_time = []
        long_exit_data = []
        long_exit_time = []
        short_entry_data = []
        short_entry_time = []
        short_exit_data = []
        short_exit_time = []


        for c in self.chart.data:
            open_data.append(c.open)
            close_data.append(c.close)
            high_data.append(c.high)
            low_data.append(c.low)
            x_data.append(tt.FloattoTime(c.start_time))
            x_data_ichimokuA.append(tt.FloattoTime(c.start_time+26*self.chart.period))
            x_data_ichimokuB.append(tt.FloattoTime(c.start_time+26*self.chart.period))

        for position in self.strategy.positions:
            if position.short:
                short_entry_data.append(position.entry_price)
                short_entry_time.append(tt.FloattoTime(position.start_time))
                if position.exitTime != 0:
                    short_exit_data.append(position.exit_price)
                    short_exit_time.append(tt.FloattoTime(position.exitTime))
            else:
                long_entry_data.append(position.entry_price)
                long_entry_time.append(tt.FloattoTime(position.start_time))
                if position.exitTime != 0:
                    long_exit_data.append(position.exit_price)
                    long_exit_time.append(tt.FloattoTime(position.exitTime))

        trace = self.plotCandle(open_data,close_data,high_data,low_data,x_data)
        # rsi,rsi_moy,rsi_min,rsi_max = self.plotRsi(close_data,x_data)
        # st,st_min,st_max = self.plotStochastique(close_data,low_data, high_data, x_data)
        shortEntryPoint, shortExitPoint = self.plotShortPosition(short_entry_data,short_entry_time,short_exit_data,short_exit_time)
        longEntryPoint, longExitPoint = self.plotLongPosition(long_entry_data,long_entry_time,long_exit_data,long_exit_time)
        # portfolio = self.plotPortfolio(close_data,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time,x_data)
        # bollingerSup,bollinger,bollingerInf = self.plotBollinger(close_data,x_data)
        # span_A,span_B = self.plotIchimoku(high_data,low_data,x_data_ichimokuA,x_data_ichimokuB)

        layout = {
            'title': self.chart.pair+" "+str(self.chart.period)+" s",
            'xaxis':{'rangeslider' : dict(visible = False)},
            'yaxis1': {'title': self.chart.pair,'domain':[0.26,1],'autorange':True},
            'yaxis2':{'domain':[0,0.25]},
            }

        layout2 = plotly.graph_objs.Layout(
            yaxis2=dict(
                overlaying='y',
                side='right'
                )
            )


        fig = plotly.tools.make_subplots(rows=2, cols=1,shared_xaxes=True)
        fig.append_trace(trace, 1, 1)
        # fig.append_trace(bollingerSup,1,1)
        # fig.append_trace(bollinger,1,1)
        # fig.append_trace(bollingerInf,1,1)
        fig.append_trace(shortEntryPoint, 1, 1)
        fig.append_trace(shortExitPoint, 1, 1)
        fig.append_trace(longEntryPoint, 1, 1)
        fig.append_trace(longExitPoint, 1, 1)
        # fig.append_trace(span_A, 1, 1)
        # fig.append_trace(span_B, 1, 1)
        # fig.append_trace(rsi, 2, 1)
        # fig.append_trace(rsi_moy, 2, 1)
        # fig.append_trace(rsi_min, 2, 1)
        # fig.append_trace(rsi_max, 2, 1)
        # fig.append_trace(st, 2, 1)
        # fig.append_trace(st_min, 2, 1)
        # fig.append_trace(st_max, 2, 1)

        fig['layout']=layout
        plotly.offline.plot(fig,filename='graphe.html')

        # fig2 = plotly.graph_objs.Figure(data=portfolio,layout=layout2)
        # plotly.offline.plot(fig2,filename='portfolio.html')
