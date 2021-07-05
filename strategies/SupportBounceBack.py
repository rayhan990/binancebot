from indicators import SupRes

class SupportBounceBack:
	def __init__(self, candles):
		self.candles = candles

	def check(self, currentPrice, bounceLevel=0.01):
		res = SupRes.Sup_Res_Finder()
		support_resistance = res.find_levels(self.candles)
		support_resistance.sort(key=lambda tup:tup[1])

		for level in support_resistance:
			levelPrice = float(level[1])
			nearLevel = levelPrice<currentPrice and (levelPrice+levelPrice*bounceLevel)>currentPrice
			
			if nearLevel and self.isPriceIncreasing(currentPrice):	#If the price is increasing and near a level
				stopLossLevel = levelPrice-levelPrice*0.005
				takeProfit = currentPrice + (currentPrice-stopLossLevel)*2

				return {
					'type' : 'L',
					'level' : level,
					'stopLoss' : stopLossLevel,
					'takeProfit' : takeProfit
				}

		return {'type' : 'U', 'level' : level, 'stopLoss' : 0, 'takeProfit' : 0}

	def isPriceIncreasing(self, currentPrice):
		return currentPrice>self.candles.iloc[-1]['Close']