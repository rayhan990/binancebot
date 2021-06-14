from datetime import datetime
from db import dbop
from tradereq import trade
from strategies import highlow
from log import email
from utils import utils
from settings import settings
import sched, time


dbop.createDb()

account = dbop.getAccountInfo(1)[0];
baseCurrency = account[3]

s = sched.scheduler(time.time, time.sleep)

def checkCoins(sc):
	availFunds = trade.getAvailableFunds(baseCurrency)
	coins = dbop.getCryptos()
	for coin in coins:
		if(utils.isTradeAllowed(coin, availFunds)):
			# Coin: 0: id, 1: name, 2: price, 3: lastupdates, 4: stake, 5: buyVariation, 6: sellVariation, 7: active
			currentPrice = trade.getCurrentPrice(coin[1])
			highlow.perform(coin, availFunds, currentPrice)
	
	try:
		checkPreviousBuyTransactions()
		checkPreviousSellTransactions()
	except Exception as ex:
		print(ex)
		email.sendErrorEmail(str(ex), 'Error')

	s.enter(settings.INTERVAL, 1, checkCoins, (sc,))
		

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
			email.sendErrorEmail(msg, 'Sell')
			print(msg)
			dbop.updateTransaction(transaction[0])

s.enter(settings.INTERVAL, 1, checkCoins, (s,))
s.run()
