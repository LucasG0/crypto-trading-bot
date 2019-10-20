import numpy as np
class BotIndicators(object):
	def __init__(self):
		self.tenkan_sen = 0
		self.kijun_sen = 0
		self.true_range = []

	def momentum(self, data_points, period=14):
		if (len(data_points) > period -1):
			return data_points[-1] * 100 / data_points[-period]

	def EMA(self, prices, period):
		x = np.asarray(prices)
		weights = None
		weights = np.exp(np.linspace(-1., 0.,min(len(prices),period) ))
		weights /= weights.sum()

		a = np.convolve(x, weights, mode='full')[:len(x)]
		a[:period] = a[period]
		return a

	def MACD(self, prices, nslow=26, nfast=12):
		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow

	def RSI(self, prices, period=14):
		deltas = np.diff(prices)
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		if down != 0:
			rs = up/down
		else:
			rs = 1
		rsi = np.zeros_like(prices)
		rsi[:period] = 100. - 100./(1. + rs)
		for i in range(period, len(prices)):
			delta = deltas[i - 1]
			if delta > 0:
				upval = delta
				downval = 0.
			else:
				upval = 0.
				downval = -delta

			up = (up*(period - 1) + upval)/period
			down = (down*(period - 1) + downval)/period
			rs = up/down
			rsi[i] = 100. - 100./(1. + rs)
		return rsi[-1]

	def simple_average(self,prices,nb_period):
		return sum(prices[-min(len(prices),nb_period):]) / float(len(prices[-min(len(prices),nb_period):]))

	def exp_average(self,prices,candlestick,nb_period,last_average):
		if lastAverage != 0:
			res = (2/float(nb_period+1))*candlestick.close+(1-2/float(nb_period+1))*last_average
		else:
			res = (candlestick.low + candlestick.high + candlestick.close)/float(3)
		return res


	def exp_moyenne(self,prices,nb_period,last_average):
		a = 2./float(nb_period+1)
		if len(prices)>nb_period:
			res = a*float(prices[-1])+(1.-a)*last_average
		else:
			res = prices[-1]
		return res

	def point_pivot(self,candlestick):
		return (candlestick.high + candlestick.low + candlestick.close)/float(3)

	def bollinger(self,prices,nb_period=20,coeff=2):
		moving_average = self.simple_average(prices,nb_period)
		sigma = 0
		L = len(prices)
		for k in range(1,min(L,nb_period+1)):
			sigma += (prices[-k] - moving_average)**2
		sigma = np.sqrt(sigma/float(nb_period))
		return [moving_average - coeff*sigma,moving_average,moving_average + coeff*sigma]

	def ichimoku(self,high,low):
		if len(high) >= 9:
			high_9 = max(high[-9:])
			low_9 = min(low[-9:])
		else:
			high_9 = max(high)
			low_9 = min(low)

		self.tenkan_sen = (high_9+low_9)/2

		if len(high) >= 26:
			high_26 = max(high[-26:])
			low_26 = min(low[-26:])
		else:
			high_26 = max(high)
			low_26 = min(low)

		self.kijun_sen = (high_26+low_26)/2

		senkou_span_A = (self.tenkan_sen+self.kijun_sen)/2

		if len(high) >= 52:
			senkou_span_B = (max(high[-52:])+min(low[-52:]))/2
		else:
			senkou_span_B = (max(high)+min(low))/2

		return [senkou_span_A,senkou_span_B]

	def stochastique(self,prices,low,high,nb_period=14):
		if (len(low)>nb_period):
			if(max(high[-nb_period:]) == min(low[-nb_period:])):
				print("len(prices) = " + str(len(prices)))
			return 100*(prices[-1]-min(low[-nb_period:]))/(max(high[-nb_period:])-min(low[-nb_period:]))
		else:
			return -1

	def average_true_range(self,high,low,prices,nb_period=20):
		L = len(prices)
		if L>1:
			self.true_range.append(max(high[-1]-low[-1],prices[-2]-high[-1],prices[-2]-low[-1]))
			return self.simple_average(self.true_range,min(L,nb_period))
		else:
			return 0

	def saitta_support_resistance(self,high,low,nb_period=20):
		if len(high)>2:
			support = min(low[-min(nb_period,len(low)):-1])
			resistance = max(high[-min(nb_period,len(high)):-1])
			return [support,resistance]
		else:
			return [0,999999999]
