from poloniex import poloniex
from urllib.request import urlopen
import json
import pprint
from botcandlestick import BotCandlestick
import time
import timetranslate as tt

# Get data (candlesticks) with given parameters from an exchange.
class BotChart(object):
	def __init__(self, exchange, pair, period, start_time=False, endTime=False, backtest=True):
		self.pair = pair
		self.period = period
		if backtest:
			self.start_time = tt.TimetoFloat(start_time)
			self.endTime = tt.TimetoFloat(endTime)
		self.compteur = 0
		self.data = []

		if (exchange == "poloniex"):
			self.conn = poloniex('key goes here','Secret goes here')
			if backtest:
				poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.start_time,"end":self.endTime,"period":self.period})
				for datum in poloData:
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],self.start_time+self.compteur*self.period,datum['weightedAverage']))
						self.compteur += 1

		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+str(self.period)+"&_="+str(self.start_time)
				response = urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]

	def get_points(self):
		return self.data

	def get_current_price(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice

	def get_sigma(self):
		volatilite = []
		for c in self.data:
			volatilite.append((c.high-c.low)/c.low*100)
		m = sum(volatilite,0.0)/len(volatilite)
		v = sum([(x-m)**2 for x in volatilite],0.0)/len(volatilite)
		s = v ** 0.5
		return s
