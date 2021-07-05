from binance.client import Client
from settings import settings
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from utils import utils

class Futures:
	def __init__(self):
		self.binance_client = Client(settings.api_key, settings.api_secret)
		pass

	def getExchange(self):
		exchangeInfo = self.binance_client.futures_exchange_info()
		symbols_n_precision = {}

		for item in exchangeInfo['symbols']:
			symbols_n_precision
			symbols_n_precision[item['symbol']] = {'pair' : item['pair'], 'precision' : item['quantityPrecision'], 'minQty' : item['filters'][1]['minQty']}

		return symbols_n_precision

	def getAvailableFunds(self, asset):
		assets = self.binance_client.futures_account_balance()
		return utils.FindAssetInAccount(asset, assets)

	def getCurrentPrice(self, symbol):
		ticker = self.binance_client.futures_ticker(symbol=symbol)
		return float(ticker['lastPrice'])

	def createBuyOrder(self, symbol, quantity, price):
		order = self.binance_client.futures_create_order(
			symbol=symbol,
			side=self.binance_client.SIDE_BUY,
			type=self.binance_client.ORDER_TYPE_LIMIT,
			quantity=quantity,
			newOrderRespType = 'FULL',
			price=price,
			timeInForce="GTC",
			leverage=1
		)

		return order

	def createSellOrder(self, symbol, quantity, price):
		order = self.binance_client.futures_create_order(
			symbol=symbol,
			side=self.binance_client.SIDE_SELL,
			type=self.binance_client.ORDER_TYPE_LIMIT,
			quantity=quantity,
			newOrderRespType = 'FULL',
			price=price,
			timeInForce="GTC",
			leverage=1
		)

		return order

	def createOrderTest(self, symbol, quantity, price):
		order = self.binance_client.create_test_order(
			symbol=symbol,
			side=self.binance_client.SIDE_BUY,
			type=self.binance_client.ORDER_TYPE_LIMIT,
			quantity=quantity,
			newOrderRespType = 'FULL',
			price=price,
			timeInForce="GTC",
			leverage=1
		)

		return order

	def get24Avg(self, symbol):
		ticker = self.binance_client.futures_ticker(symbol=symbol)
		return float(ticker['weightedAvgPrice'])

	def getOrder(self, orderId, symbol):
		order = self.binance_client.futures_get_order(orderId=orderId, symbol=symbol)
		
		return order

	def getCandles(self, symbol, interval='1d', limit=200):
		candles = self.binance_client.futures_klines(symbol=symbol, interval=interval, limit=limit)

		data = np.array(candles)
		dataset = pd.DataFrame({
			'Open_time': data[:, 0],
			'Open': data[:, 1],
			'High': data[:, 2],
			'Low': data[:, 3],
			'Close': data[:, 4],
			'Volume': data[:, 5],
			'Close_time': data[:, 6],
			'Quote_asset_volume': data[:, 7],
			'Number_of_trades': data[:, 8],
			'Taker_buy_base_asset_volume': data[:, 9],
			'Taker_buy_quote_asset_volume': data[:, 10],
			'Can_be_ignored': data[:, 11]
		})

		dataset['Open_time'] = pd.to_datetime(dataset['Open_time'].astype('float64'), unit='ns')
		dataset['High'] = dataset['High'].astype('float64')
		dataset['Low'] = dataset['Low'].astype('float64')
		dataset['Open'] = dataset['Open'].astype('float64')
		dataset['Close'] = dataset['Close'].astype('float64')
		dataset['Volume'] = dataset['Volume'].astype('float64')

		return dataset
