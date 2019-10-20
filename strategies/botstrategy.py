from botlog import BotLog
from botindicators import BotIndicators
from botposition import BotPosition

# Inherit this class to create a new trading strategy.
# conditionOpen and conditionClose need to be overriden.
class BotStrategy(object):
	def __init__(self):
		self.result = 0
		self.output = BotLog()
		self.prices = []
		self.positions = []
		self.low = []
		self.high = []
		self.current_price = ""
		self.indicators = BotIndicators()
		self.num_simulpositions = 1

	def tick(self,candlestick):
		self.current_price = float(candlestick.close)
		self.prices.append(self.current_price)
		self.low.append(candlestick.low)
		self.high.append(candlestick.high)
		self.evaluate_positions(candlestick)
		self.update_openpositions(candlestick)
		# self.showPositions()


	# Update position status. Only one position is currently supported.
	def evaluate_positions(self,candlestick):
		openpositions = []
		for position in self.positions:
			if (position.status == "OPEN"):
				openpositions.append(position)
		if (len(openpositions) < self.num_simulpositions):
			position = self.open_position(candlestick)
			if position != None:
				self.positions.append(position)
		for open_pos in openpositions:
			self.try_close_position(open_pos,candlestick)

	def update_openpositions(self,candlestick):
		for position in self.positions:
			if (position.status == "OPEN"):
				position.tick(self.current_price,candlestick)

	def show_positions(self):
		for position in self.positions:
			position.showposition()

	def get_result(self):
		res = 0
		for position in self.positions:
			if position.short:
				res += position.entry_price
				res -= position.exit_price
			else:
				res -= position.entry_price
				res += position.exit_price
		return res

	def open_position(self):
		raise NotImplementedError

	def close_position(self):
		return False
