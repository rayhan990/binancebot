from binance.client import Client
from settings import settings
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

binance_client = Client(settings.api_key, settings.api_secret)

def getCurrentPrice(currency):
	currentPrice = binance_client.get_symbol_ticker(symbol=currency)
	return float(currentPrice['price'])

def getAvailableFunds(asset):
	fund = binance_client.get_asset_balance(asset)
	return float(fund['free'])

def createBuyOrder(symbol, quantity, price):
	print(quantity)
	order = binance_client.create_order(
		symbol=symbol,
		side=binance_client.SIDE_BUY,
		type=binance_client.ORDER_TYPE_LIMIT,
		quantity=quantity,
		newOrderRespType = 'FULL',
		price=price,
		timeInForce="GTC"
	)

	return order

def createSellOrder(symbol, quantity, price):
	order = binance_client.create_order(
		symbol=symbol,
		side=binance_client.SIDE_SELL,
		type=binance_client.ORDER_TYPE_LIMIT,
		quantity=quantity,
		newOrderRespType = 'FULL',
		price=price,
		timeInForce="GTC"
	)

	return order

def createOrderTest(symbol, quantity, price):
	order = binance_client.create_test_order(
		symbol=symbol,
		side=binance_client.SIDE_BUY,
		type=binance_client.ORDER_TYPE_LIMIT,
		quantity=quantity,
		newOrderRespType = 'FULL',
		price=price,
		timeInForce="GTC"
	)

	return order

def get24Avg(symbol):
	ticker = binance_client.get_ticker(symbol=symbol)
	return float(ticker['weightedAvgPrice'])

def getOrder(orderId, symbol):
	order = binance_client.get_order(orderId =orderId, symbol=symbol)
	
	return order

def performPurchase(coin, currentPrice, availFunds):
	stakeAmount = (availFunds/100) * coin[4]
	if stakeAmount<settings.MIN_BALANCE:
		stakeAmount = settings.MIN_BALANCE+1
		print("stake", stakeAmount)

	stake = round(stakeAmount/currentPrice, 2)

	if stake==0:
		stake = round(stakeAmount/currentPrice, 3)

	if stake>1:
		stake = round(stakeAmount/currentPrice, 0)

	print("%s %f Buy now! @ %f" %(coin[1], stake, currentPrice))
	order = createBuyOrder(coin[1], stake, currentPrice)
	return order

def getCandles(symbol, interval='1d', limit=200):
	candles = binance_client.get_klines(symbol=symbol, interval=interval, limit=limit)

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
