import sqlite3 as sl
from db import dbop
from settings import settings


dbop.createState("ETHUSDT", 20, 5, 4)
dbop.createState("BTCUSDT", 20, 5, 4)
dbop.createState("BNBUSDT", 20, 5, 4)
dbop.createState("ADAUSDT", 10, 5, 5)
dbop.createState("XRPUSDT", 5, 5, 5)
dbop.createState("DOGEUSDT", 5, 5, 5)


api_key=settings.api_key
api_secret=settings.api_secret

dbop.createAccount(api_key, api_secret, "USDT")