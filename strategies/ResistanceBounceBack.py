from indicators import SupRes

class ResistanceBounceBack:
	def __init__(self, candles):
		self.candles = candles

	def check(self, currentPrice, bounceLevel=0.01):
		res = SupRes.Sup_Res_Finder()
		support_resistance = res.find_levels(self.candles)
		support_resistance.sort(key=lambda tup:tup[1])

		for level in support_resistance:
			levelPrice = float(level[1])
			nearLevel = (levelPrice)>currentPrice and (levelPrice-levelPrice*bounceLevel)<currentPrice
			
			stopLossLevel = levelPrice+levelPrice*0.005
			takeProfit = currentPrice - (stopLossLevel-currentPrice)*2

			if nearLevel and self.isPriceDecreasing(currentPrice):	#If the price is increasing and near a level
				return {
					'type' : 'S',
					'level' : level,
					'stopLoss' : stopLossLevel,
					'takeProfit' : takeProfit
				}

		return {'type' : 'U', 'level' : level, 'stopLoss' : 0, 'takeProfit' : 0}

	def isPriceDecreasing(self, currentPrice):
		return currentPrice<self.candles.iloc[-1]['Close']