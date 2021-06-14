from settings import settings

def isTradeAllowed(coin, availFunds):
	canTrade = True
	if(availFunds<settings.MIN_BALANCE):
		canTrade = False

	return canTrade