import sys, getopt
import time

from botlog import BotLog

# Candlestick object with several attributes that may be useful for trading strategies.
class BotCandlestick(object):
	def __init__(self, period=300,open=None,close=None,high=None,low=None,start_time=time.time(),price_average=None):
		self.current = None
		self.open = open
		self.close = close
		self.high = high
		self.low = low
		self.start_time = start_time
		self.period = period
		self.output = BotLog()
		self.price_average = price_average

	def tick(self,price):
		self.current = float(price)
		if (self.open is None):
			self.open = self.current
		if ( (self.high is None) or (self.current > self.high) ):
			self.high = self.current
		if ( (self.low is None) or (self.current < self.low) ):
			self.low = self.current
		if ( time.time() >= ( self.start_time + self.period) ):
			self.close = self.current
			self.price_average = ( self.high + self.low + self.close ) / float(3)

		self.output.log("Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low)+" Current: "+str(self.current))

	def is_closed(self):
		if (self.close is not None):
			return True
		else:
			return False
