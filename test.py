from strategies import macd
from indicators import SupRes

x = macd.check([0, 'BTCUSDT'], 0)
res = SupRes.Sup_Res_Finder()

levels = res.find_levels(x)
print(levels)