from settings import settings
from db import dbop

def isTradeAllowed(coin, availFunds):
	if(availFunds<settings.MIN_BALANCE):
		return False

	if dbop.countOutstandingOrders(coin[1], 'SELL')>=2:
		return False

	return True