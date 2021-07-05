from db import dbop
from settings import settings
from utils import ApplyStrategies
import sched, time
# from log import email

dbop.createDb()

account = dbop.getAccountInfo(1)[0];
baseCurrency = account[3]

s = sched.scheduler(time.time, time.sleep)

def checkCoins(sc):
	try:
		results = ApplyStrategies.applyStrategies(baseCurrency)


		ApplyStrategies.checkPreviousBuyTransactions()
		ApplyStrategies.checkPreviousSellTransactions()
	except Exception as ex:
		print(ex)
		email.sendEmailAlert(str(ex), 'Error')

	s.enter(settings.INTERVAL, 1, checkCoins, (sc,))

s.enter(settings.INTERVAL, 1, checkCoins, (s,))
s.run()