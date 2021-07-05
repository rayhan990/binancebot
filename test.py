from db import dbop
from utils import utils
from tradereq import futures
from strategies import BounceFromKeyLevel
from strategies import SupResBounceRsiDivergence


future_client = futures.Futures();
futuresexchange = future_client.getExchange()

coins = dbop.getCryptos()

for coin in coins:
	availFunds = float(future_client.getAvailableFunds('USDT')['balance'])
	# Strategies
	supResBounceRsiDivergence = SupResBounceRsiDivergence.SupResBounceRsiDivergence(future_client, coin, '1d', '15m')
	bounceFromKeyLevel = BounceFromKeyLevel.BounceFromKeyLevel(future_client, coin, '1d')

	strategies = [
		{
			'name' : 'SuppResBounceRsiDivergence',
			'strategyInstance' : supResBounceRsiDivergence
		},
		{
			'name' : 'default',
			'strategyInstance' : bounceFromKeyLevel
		}
	]

	currentPrice = future_client.getCurrentPrice(coin[1])
	stake = utils.calculateStake(availFunds, currentPrice, coin[4])

	for strategy in strategies:
		isTreadingAllowed = utils.isTradeAllowed(coin[1], availFunds, strategy['name'])
		if isTreadingAllowed:
			result = strategy['strategyInstance'].check()

			if result['type']=='L':
				print("Long with %s" %strategy['name'])
				order = futures.createBuyOrder(coin[1], coin[1], currentPrice)
				registerPuchase(order, currentPrice, strategy['name'])
			if result['type']=='S':
				print("Shorting with %s" %strategy['name'])
				order = futures.createSellOrder(coin[1], coin[1],currentPrice)
				registerPuchase(order, currentPrice, strategy['name'])