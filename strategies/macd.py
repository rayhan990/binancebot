from tradereq import trade
from db import dbop
from log import email
import numpy as np
import pandas as pd
import pandas_ta as ta

def check(coin, currentPrice):
	candles = trade.getCandles(coin[1])
	data = np.array(candles)
	dataset = pd.DataFrame({
		'Open_time': data[:, 0],
		'Open': data[:, 1],
		'High': data[:, 2],
		'Low': data[:, 3],
		'Close': data[:, 4],
		'Volume': data[:, 5],
		'Close_time': data[:, 6]
		# 'Quote_asset_volume': data[:, 7],
		# 'Number_of_trades': data[:, 8],
		# 'Taker_buy_base_asset_volume': data[:, 9],
		# 'Taker_buy_quote_asset_volume': data[:, 10],
		# 'Can_be_ignored': data[:, 11]
	})
	dataset['Open_time'] = pd.to_datetime(dataset['Open_time'].astype('float64'), unit='ns')
	dataset['High'] = dataset['High'].astype('float64')
	dataset['Low'] = dataset['Low'].astype('float64')
	dataset['Open'] = dataset['Open'].astype('float64')
	dataset['Close'] = dataset['Close'].astype('float64')
	dataset['Volume'] = dataset['Volume'].astype('float64')

	return dataset

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