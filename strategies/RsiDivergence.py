import pandas_ta as ta
from utils import utils
from datetime import datetime

class RsiDivergence:
	def __init__(self, client, coin):
		self.coin  = coin
		self.client = client
		self.candles = self.client.getCandles(coin)
		pass

	def check(self, interval, variationAcceptance=2):
		#variationAcceptance: Acceptance criteria for the result, increments of the interval
		# Compares the rsi for the coin and the interval
		additionalDataType='Close_time'
		currentPrice = self.client.getCurrentPrice(self.coin)

		rsi = ta.momentum.rsi(self.candles['High'], additionalData=self.candles[additionalDataType])

		hlws = utils.getHighsAndLows(self.candles['Low'], additionalData=self.candles[additionalDataType])
		rsihlws = utils.getHighsAndLows(rsi)

		msSinceFromVerification = datetime.now().timestamp() * 1000 - float(hlws['AdditionalData'][0])
		intervalMs = utils.inteval2Milliseconds(interval)

		if msSinceFromVerification/intervalMs<=variationAcceptance*intervalMs:	#Trade accepted only within the time variance from the original interval
			variationType = 'L' if hlws['Type'][0]=='L' and rsihlws['Type'][0]=='H' else 'S'
			return {'type' : variationType, 'RsiValue' : rsihlws['Value'][0]}
		else:
			return {'type' : 'U', 'RsiValue' : 0}