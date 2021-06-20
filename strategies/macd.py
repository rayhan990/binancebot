from tradereq import trade
from db import dbop
from log import email
import pandas as pd
import pandas_ta as ta

def check(coin, currentPrice):
	candles = trade.getCandles(coin[1])

	return candles

def findSmas(dataset):
	dataset.set_index(pd.DatetimeIndex(pd.to_datetime(dataset["Open_time"].dt.date)), inplace=True)	
	dataset.ta.strategy(ta.CommonStrategy)
	print(dataset)

	return dataset

def perform(coin, availFunds, currentPrice):
	if(currentPrice>coin[2]):
		dbop.updateState(coin[1], currentPrice)

	if check(coin, currentPrice):
		try:
			order = trade.performPurchase(coin, currentPrice, availFunds)
			dbop.updateState(coin[1], currentPrice)

			targetPrice = currentPrice + ((currentPrice/100) * coin[6])
			dbop.createTransacrtion(coin[1], "BUY", currentPrice, order["orderId"], order["clientOrderId"], 1, targetPrice)
		except Exception as ex:
			email.sendEmailAlert(str(ex), 'Error')
			print(ex)