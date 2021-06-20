# https://www.youtube.com/watch?v=QdbKApfwF-g

# https://www.youtube.com/watch?v=4dVB_g5YeSE&t=703s

from strategies import PriceAction
from tradereq import trade
import pandas_ta as ta
import pandas as pd
from utils import utils
import datetime

# def 
coin = 'BTCUSDT'
candles = trade.getCandles(coin)
currentPrice = trade.getCurrentPrice(coin)

candles = trade.getCandles(coin, interval='1d')
rsi = ta.momentum.rsi(candles['High'], additionalData=candles['Close_time'])
print(rsi)

hlws = utils.getHighsAndLows(candles['Low'], additionalData=candles['Close_time'])
rsihlws = utils.getHighsAndLows(rsi)

Enter = False
PrevVal = 0
for (x,y, z, j, s) in zip(hlws['Type'], rsihlws['Type'], hlws['AdditionalData'], hlws['Price'], rsihlws['Price']):
	if Enter:
		Enter = False
		print("Exiting @ %s %s %s %f" %(z, j, s, (100*(float(j)-float(PrevVal)))/float(PrevVal)))
	if x=='L' and y=='H':
		print("Entering @ ", z, j)
		PrevVal = j
		Enter = True


# print(x)

# print(hlws.compare(rsihlws))