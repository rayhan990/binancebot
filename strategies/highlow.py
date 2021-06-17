from tradereq import trade
from db import dbop
from log import email

def check(coin, currentPrice):
	minTargetPrice = coin[2]-((coin[2]/100)*coin[5])
	return currentPrice<minTargetPrice

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