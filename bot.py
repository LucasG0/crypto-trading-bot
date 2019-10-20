import sys
import argparse
import time
import pprint

from urllib.error import URLError
from botchart import BotChart
from strategies.botstrategy import BotStrategy
from strategies import SLSTM
from botlog import BotLog
from botcandlestick import BotCandlestick
from plotgraphe import PlotGraphe


# Run bot, parameters can be specified in command line.
def main(argv):
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--period", help="Period length in seconds, 14400 by default", type=int, choices=[7200,14400,86400],default=7200)
		parser.add_argument("-c", "--currency", help="Currency pair | Ex: BTC_ETH", default='BTC_ETH')
		parser.add_argument("-s", "--start", help="Start time in YYYY-MM-DD HH:MM:SS (for backtesting), '2016-11-02 14:00:00' by default",default='2016-11-02 14:00:00')
		parser.add_argument("-e", "--end", help="End time in YYYY-MM-DD HH:MM:SS (for backtesting), '2018-12-14 20:53:20' by default",default='2018-12-14 20:53:20')
		args = vars(parser.parse_args())
	except:
		print("ArgumentParser Error type -h for help")
		sys.exit(2)

	pair = args["currency"]
	period = args["period"]
	debut = args['start']
	fin = args['end']
	chart = BotChart("poloniex",pair,period,debut,fin)
	strategy = SLSTM.SLSTM()
	for candlestick in chart.get_points():
		strategy.tick(candlestick)
	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()
	print("Result = " + str(strategy.get_result()) + " BTC")
	try:
		sigma = chart.getSigma()*float(chart.compteur)**0.5
		perf = graphe.perf
		sharpe_ratio = perf/sigma
		print("\n Performance: "+str(perf))
		print("\n Ratio de Sharpe: "+str(sharpe_ratio)+"\n")
	except Exception as e:
		pass

if __name__ == "__main__":
	main(sys.argv[1:])
