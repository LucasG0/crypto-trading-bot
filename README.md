# Crypto Currency Trading Bot

A little side-project called **Zbot** inspired by github user @bwentzloff.

Created with @Adriy1


## Description

A trading bot which can take buy or short positions. It features:
- Semi-Automated Trading (only signals for now)
- Strategies based on financial indicators or deep learning (LSTM)
- Support of Poloniex exchange
- Easy way to implement new strategies (with Python classes)
- Easy backtesting with graphical interface using plot.ly library
- Graphical evolution of portfolio and calculation of Sharpe Ratio
- Everything is configurable (stoploss,period,pair)
- Many indicators (RSI,MACD,EMA,Ichimoku...)
- Can send notifications on phone with PushBullet API

## Disclaimer

Use at your own risk, the strategies always need to be backtested. We consider this bot as a tool to help our decisions.

## Requirements

- Python 3.5.2 with pip3
- Plot.ly  `pip3 install plotly`
- Numpy `pip3 install numpy`
- pyPushBullet from @Alzerphur `pip3 install git+https://github.com/Azelphur/pyPushBullet.git` (optional)

## How to run it ?

To launch Zbot, just run `python3 bot.py`

To show the help `python3 bot.py -h`

    usage:  python bot.py [-h] [-p {300,900,1800,7200,14400,86400}] [-c CURRENCY] [-b]
              [-s START] [-e END] [-S]

    optional arguments:
              -h, --help            show this help message and exit

              -p {7200,14400,86400}, --period {300,900,1800,7200,14400,86400}
                    Period length in seconds, 14400 by default


              -c CURRENCY, --currency CURRENCY
                                Currency pair | Ex: USDT_ETH

              -s START, --start START
                                Start time in YYYY-MM-DD HH:MM:SS (for backtesting),
                                '2016-11-02 14:00:00' by default

              -e END, --end END     End time in YYYY-MM-DD HH:MM:SS (for backtesting),
                                '2018-12-14 20:53:20' by default

              -S, --short           Enable Short Mode

A trained regression model is provided, but you can also run lstm_classification and lstm_regression to train models with different parameters.


### Using graphical interface

You can configure the result of backtesting and plot whatever you want by changing the file plotgraphe.py. It's using the plotly library.

### Creating new strategies

We higly recommend to create a new child class of BotStrategy for each strategie created. You simply have to implement `open_position()` and `try_close_position()` in the child class and select this class when you assign the strategy variable in bot.py.

### API PushBullet

Don't forget to put your api key in a file called api.txt to use PushBullet notifications.

## To Do List
- Improve existing strategies
- Create new strategies
- Support more exchanges
- Fully-automated trading on exchanges
- Integrate exchange fees in backtesting
- Create a web interface to manage the bot

### End
