from strategies import macd
from indicators import SupRes
from tradereq import trade

class PriceAction:
	def __init__(self, candles):
		self.candles = candles

	def SupportResistanceBounceBack(self, currentPrice, bounceLevel=0.01):
		res = SupRes.Sup_Res_Finder()
		support_resistance = res.find_levels(self.candles)
		support_resistance.sort(key=lambda tup:tup[1])

		for level in support_resistance:
			nearLevel = (level[1])<currentPrice and (level[1]+level[1]*bounceLevel)>currentPrice
			
			if nearLevel and self.isPriceIncreasing(currentPrice):	#If the price is increasing and near a level
				return True

		return False

	def isPriceIncreasing(self, currentPrice):
		return currentPrice>self.candles.iloc[-1]['Close']