# https://www.youtube.com/watch?v=QdbKApfwF-g
# https://www.youtube.com/watch?v=4dVB_g5YeSE&t=703s

from strategies import RsiDivergence
from strategies import SupportBounceBack
from utils import utils
from indicators import SupRes
from strategies import BounceFromKeyLevel

class SupResBounceRsiDivergence:
	def __init__(self, client, coin, long_interval='1d', short_interval='1h'):
		self.symbol  = coin[1]
		self.coin = coin
		self.long_interval = '1d'
		self.short_interval = '1h'
		self.client = client
		self.candles = self.client.getCandles(self.symbol, interval=self.long_interval)
		pass
	
	def check(self):
		candles = self.client.getCandles(self.symbol, interval=self.short_interval)
		currentPrice = self.client.getCurrentPrice(self.symbol)
		rsiDivergence = RsiDivergence.RsiDivergence(self.client, self.symbol)
		
		bounceFromKeyLevel = BounceFromKeyLevel.BounceFromKeyLevel(self.client, self.coin, self.long_interval)
		isPriceBouncingBackFromSupport = bounceFromKeyLevel.check()

		if isPriceBouncingBackFromSupport['type']!='U':
			return rsiDivergence.check(self.short_interval)
		else:
			return {'type' : 'U', 'RsiValue' : 0, 'stopLoss' : 0, 'profitLevel' : 0}

	def confirm(self):
		candles = self.client.getCandles(self.symbol, interval=self.short_interval)
		supresFinder = SupRes.Sup_Res_Finder()
		supRes = supresFinder.find_levels(candles)
		currentPrice = self.client.getCurrentPrice(self.symbol)

		ax = supRes[-2][0]
		bx = supRes[-1][0]
		ay = supRes[-2][1]
		by = supRes[-1][1]
		x = 200

		minPrice = ((((x-ax)/(bx-ax))*(by-ay))+ay)

		return ay<by and currentPrice>=minPrice