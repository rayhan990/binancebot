from settings import settings
from db import dbop

def isTradeAllowed(coin, availFunds):
	if(availFunds<settings.MIN_BALANCE):
		return False
	print(coin[1])
	print(dbop.countOutstandingOrders(coin[1], 'SELL'))

	if dbop.countOutstandingOrders(coin[1], 'SELL')>=2:
		return False

	return True