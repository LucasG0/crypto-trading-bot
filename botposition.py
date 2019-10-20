from botlog import BotLog

# Position object represented by an entry and an exit.
class BotPosition(object):
	def __init__(self,current_price,start_time,short,takeProfit=0,stopLoss=0):
		self.output = BotLog()
		self.status = "OPEN"
		self.entry_price = current_price
		self.exit_price = 0.
		self.start_time = start_time
		self.exitTime = 0.
		self.stopLoss = stopLoss
		self.takeProfit = takeProfit
		self.short = short
		if short:
			self.output.log("OPEN SELL : " + str(self.entry_price))
		else:
			self.output.log("OPEN BUY : " + str(self.entry_price))

	def close(self,current_price,endTime):
		self.status = "CLOSED"
		self.exit_price = current_price
		self.exitTime = endTime
		if self.short:
			self.output.log("CLOSE BUY : " +str(current_price) + "\n")
		else:
			self.output.log("CLOSE SELL : " +str(current_price) + "\n")


	def tick(self, current_price,candlestick):
		if self.stopLoss != 0:
			if self.short and current_price > self.stopLoss:
				self.close(current_price,candlestick.start_time)
				return
			elif not(self.short) and current_price < self.stopLoss:
				self.close(current_price,candlestick.start_time)
				return
		if self.takeProfit != 0:
			if self.short and current_price < self.takeProfit:
				self.close(current_price,candlestick.start_time)
				return
			elif not(self.short) and current_price > self.takeProfit:
				self.close(current_price,candlestick.start_time)
				return



	def showTrade(self):
		tradeStatus = "Entry Price: "+str(self.entry_price)+" Status: "+str(self.status)+" Exit Price: "+str(self.exit_price)

		if (self.status == "CLOSED"):
			tradeStatus = tradeStatus + " Profit: "
			if (self.exit_price > self.entry_price):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			tradeStatus = tradeStatus+str(self.exit_price - self.entry_price)+"\033[0m"

		# self.output.log(tradeStatus)
