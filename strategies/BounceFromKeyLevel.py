from db import dbop
from log import email
from utils import utils
from strategies import SupportBounceBack
from strategies import ResistanceBounceBack

class BounceFromKeyLevel:
	def __init__(self, client, coin, currentPrice, interval='1d'):
		self.coin  = coin
		self.interval = '1h'
		self.client = client
		pass

	def check(self):
		coin = self.coin
		minEntryPrice = coin[2]-((coin[2]/100)*coin[5])
		maxEntryPrice = coin[2]+((coin[2]/100)*coin[5])
		
		currentPrice = self.client.getCurrentPrice(coin[1])
		candles = self.client.getCandles(coin[1], interval=self.interval)
		supportBounceBack = SupportBounceBack.SupportBounceBack(candles)
		supportBounceBackResult = supportBounceBack.check(currentPrice)

		resistanceBounceBack = ResistanceBounceBack.ResistanceBounceBack(candles)
		resistanceBounceBackResult = resistanceBounceBack.check(currentPrice)

		if currentPrice<minEntryPrice and supportBounceBackResult['type']=='L':
			return {'type' : 'L', 'entryPrice' : minEntryPrice, 'stopLoss' : supportBounceBackResult['stopLoss'], 'takeProfit' : supportBounceBackResult['takeProfit']}
		elif currentPrice>maxEntryPrice  and resistanceBounceBackResult['type']=='S':
			return {'type' : 'S', 'entryPrice' : maxEntryPrice, 'stopLoss' : resistanceBounceBackResult['stopLoss'], 'takeProfit' : resistanceBounceBackResult['takeProfit']}
		else:
			return {'type' : 'U', 'entryPrice' : 0, 'stopLoss' : 0, 'takeProfit' : 0}