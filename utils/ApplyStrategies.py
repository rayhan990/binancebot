from datetime import datetime
from db import dbop
from tradereq import trade
from strategies import BounceFromKeyLevel
from strategies import SupResBounceRsiDivergence
from utils import utils
from log import email
from tradereq import futures

future_client = futures.Futures();

def applyStrategies(baseCurrency):
	coins = dbop.getCryptos()
	results = []

	for coin in coins:
		future_client.fixLeverage(coin[1], 1)
		future_client.getAvailableFunds(baseCurrency)
		availFunds = float(future_client.getAvailableFunds(baseCurrency)['balance'])
		# Strategies
		supResBounceRsiDivergence = SupResBounceRsiDivergence.SupResBounceRsiDivergence(future_client, coin, '1d', '15m')
		bounceFromKeyLevel = BounceFromKeyLevel.BounceFromKeyLevel(future_client, coin, '1d')

		strategies = [
			{
				'name' : 'SuppResBounceRsiDivergence',
				'strategyInstance' : supResBounceRsiDivergence
			},
			{
				'name' : 'bounceFromKeyLevel',
				'strategyInstance' : bounceFromKeyLevel
			}
		]

		currentPrice = future_client.getCurrentPrice(coin[1])
		stake = utils.calculateStake(availFunds, currentPrice, coin[4])

		for strategy in strategies:
			isTreadingAllowed = utils.isTradeAllowed(coin[1], availFunds, strategy['name'])
			if isTreadingAllowed:
				result = strategy['strategyInstance'].check()

				if result['type']=='L':
					print("Long with %s" %strategy['name'])
					order = future_client.createBuyOrder(coin[1], stake, currentPrice)
					utils.registerPuchase(order, currentPrice, strategy['name'])
				if result['type']=='S':
					print("Shorting with %s" %strategy['name'])
					order = future_client.createSellOrder(coin[1], stake,currentPrice)
					utils.registerPuchase(order, currentPrice, strategy['name'])

def checkPreviousBuyTransactions():
	for transaction in dbop.getTransactions("BUY"):
		order = trade.getOrder(transaction[5], transaction[1])
		targetPrice = round(transaction[6], 2)
		
		if order["status"]=="FILLED":
			print("Selling %s @ %.2f" %(transaction[1], targetPrice))
			dbop.updateTransaction(transaction[0])
			order = trade.createSellOrder(transaction[1], order["executedQty"], targetPrice)
			dbop.createTransacrtion(transaction[1], "SELL", targetPrice, order["orderId"], order["clientOrderId"], 1, targetPrice)

def checkPreviousSellTransactions():
	for transaction in dbop.getTransactions("SELL"):
		order = trade.getOrder(transaction[5], transaction[1])
		
		if order["status"]=="FILLED":
			msg = "Sold %s @ %.2f" %(transaction[1], transaction[6])
			email.sendEmailAlert(msg, 'Sell')
			dbop.updateTransaction(transaction[0])