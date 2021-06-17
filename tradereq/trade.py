from binance.client import Client
from settings import settings

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
		stakeAmount = settings.MIN_BALANCE

	stake = round(stakeAmount/currentPrice, 2)

	if stake==0:
		stake = round(stakeAmount/currentPrice, 3)

	if stake>1:
		stake = round(stakeAmount/currentPrice, 1)

	print("%s %f Buy now! @ %f" %(coin[1], stake, currentPrice))
	order = createBuyOrder(coin[1], stake, currentPrice)
	return order