from settings import settings
from db import dbop
import numpy as np
import pandas as pd
from log import email

def isTradeAllowed(symbol, availFunds, strategy):
	if(availFunds<settings.MIN_BALANCE):
		return False
	
	activeOrdersWithThisStrategy = dbop.countOutstandingOrders(symbol, strategy)
	if type(activeOrdersWithThisStrategy)==type(2) and activeOrdersWithThisStrategy>=1:
		return False

	return True

def getHighsAndLows(values, precision=2, additionalData=[]):
	hlws = []
	for x in range(0,len(values)-precision):
		isHigh = True
		isLow = True
		for y in range(0, precision):
			isHigh = isHigh and values[x+y+1]<values[x+y]
			isLow = isLow and values[x+y+1]>values[x+y]

		if x>1:
			for y in range(0, precision):
				isHigh = isHigh and values[x-y-1]<values[x-y]
				isLow = isLow and values[x-y-1]>values[x-y]

		if isHigh:
			listToAppend = [x,"H", values[x]]
			listToAppend.append(additionalData[x] if len(additionalData)>x else 0)
			hlws.append(listToAppend)
		if isLow:
			listToAppend = [x,"L", values[x]]
			listToAppend.append(additionalData[x] if len(additionalData)>x else 0)
			hlws.append(listToAppend)

	hlws = np.array(hlws)
	hlws = pd.DataFrame({
		'Type' : hlws[:,1],
		'Index' : hlws[:,0],
		'Value' : hlws[:,2],
		'AdditionalData' : hlws[:,3],
	})

	return hlws

def inteval2Milliseconds(interval):
	if interval=='1m':
		return 60*1000
	elif interval=='3m':
		return 60*1000*3
	elif interval=='5m':
		return 60*1000*5
	elif interval=='15m':
		return 60*1000*15
	elif interval=='30m':
		return 60*1000*30
	elif interval=='1h':
		return 60*1000*60
	elif interval=='2h':
		return 60*1000*120
	elif interval=='4h':
		return 60*1000*240
	elif interval=='6h':
		return 60*1000*360
	elif interval=='8h':
		return 60*1000*480
	elif interval=='12h':
		return 60*1000*720
	elif interval=='1d':
		return 60*1000*1440
	elif interval=='3d':
		return 60*1000*1440*3
	elif interval=='1w':
		return 60*1000*1440*7
	elif interval=='1M':
		return 60*1000*1440*30

def registerPuchase(order, currentPrice, strategy):
	try:
		dbop.updateState(order['symbol'], currentPrice)
		dbop.createTransacrtion(order['symbol'], order['side'], currentPrice, order["orderId"], order["clientOrderId"], 1, 0, strategy)
	except Exception as ex:
		email.sendEmailAlert(str(ex), 'Error')
		print(ex)

def FindAssetInAccount(asset, assets):
	for x in assets:
		if x['asset']==asset:
			return x
	pass

def calculateStake(availFunds, currentPrice, stakePercentage):
	stakeAmount = (availFunds/100) * stakePercentage
	if stakeAmount<settings.MIN_BALANCE:
		stakeAmount = settings.MIN_BALANCE+1

	stake = round(stakeAmount/currentPrice, 2)

	if stake==0:
		stake = round(stakeAmount/currentPrice, 3)

	if stake>1:
		stake = round(stakeAmount/currentPrice, 0)

	return stake