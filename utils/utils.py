from settings import settings
from db import dbop
import numpy as np
import pandas as pd

def isTradeAllowed(coin, availFunds):
	if(availFunds<settings.MIN_BALANCE):
		return False
		
	if dbop.countOutstandingOrders(coin[1], 'SELL')>=2:
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
		'Price' : hlws[:,2],
		'AdditionalData' : hlws[:,3],
	})

	return hlws
