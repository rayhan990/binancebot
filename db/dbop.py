import sqlite3 as sl
import pytz
from tradereq import trade
from tradereq import trade
from datetime import datetime

def createDb():
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    try:
        cur.execute("""CREATE TABLE Account (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                secret TEXT,
                currency TEXT,
                funds REAL
            );""")

        cur.execute("""
            CREATE TABLE Transactions (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                operation INTEGER,
                lastPrice REAL,
                transactionHash TEXT,
                transactionId INTEGER,
                targetPrice REAL,
                active INTEGER
            );
        """)

        cur.execute("""
            CREATE TABLE State (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE,
                lastPrice REAL,
                lastUpdate TEXT,
                stake REAL,
                buyVariation REAL,
                sellVariation REAL,
                active INTEGER
            );
        """)
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()

def getCryptos():
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    try:
        cur.execute("select * from State")
        res = cur.fetchall()

        return res
    except Exception as ex:
        sendErrorEmail(str(ex))
        return []
    finally:
        if con:
            con.close()

def getTransactions(operation):
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    try:
        stmt = "select * from Transactions WHERE active=1 AND operation='%s'" %operation
        cur.execute(stmt)
        res = cur.fetchall()

        return res
    except Exception as ex:
        print(ex)
        return []
    finally:
        if con:
            con.close()

def getAccountInfo(id):
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    try:
        cur.execute("select * from Account where id=%d" %id)
        res = cur.fetchall()

        return res
    except Exception as ex:
        print(ex)
        return []
    finally:
        if con:
            con.close()

def createTransacrtion(symbol, operation, lastPrice, transactionId, transactionHash, active, targetPrice):
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    stmt = """
        INSERT INTO Transactions (symbol, operation, lastPrice, active, transactionId, transactionHash, targetPrice) 
        VALUES ('%s', '%s', %f, %d, %d, '%s', %f)""" %(symbol, operation, lastPrice, active, transactionId, transactionHash, targetPrice)

    try:
        con.execute(stmt)
        con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()

def updateTransaction(transactionId):
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    stmt = """UPDATE Transactions SET active=0 WHERE id=%d""" %transactionId

    try:
        con.execute(stmt)
        con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()

def createState(symbol, stake, buyVar, sellVar):
    utc = pytz.utc

    con = sl.connect('./db/mydb.db')
    cur = con.cursor()
    ticker = trade.get24Avg(symbol)

    stmt = """
        INSERT INTO State 
        (symbol, active, lastPrice, lastUpdate, stake, buyVariation, sellVariation)
        VALUES ('%s', %f, %f, '%s', %f, %f, %f)""" %(symbol, 1, ticker, datetime.now(tz=utc), stake, buyVar, sellVar)
    try:
        con.execute(stmt)
        con.commit()
    except Exception as ex:
        try:
            print("updating existing values for %s" %symbol)
            stmt = """
                UPDATE State SET 
                symbol='%s', active=%d, lastPrice=%f, lastUpdate='%s', stake=%f, buyVariation=%f, sellVariation=%f WHERE symbol='%s'
            """ %(symbol, 1, float(ticker), datetime.now(tz=utc), stake, buyVar, sellVar, symbol)

            con.execute(stmt)
            con.commit()
        except Exception as secondEx:
            print(secondEx)
    finally:
        if con:
            con.close()

def updateState(coin, currentPrice):
    utc = pytz.utc
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    try:
        stmt = """
            UPDATE State SET 
            lastPrice=%f, lastUpdate='%s' WHERE symbol='%s'
        """ %(currentPrice, datetime.now(tz=utc), coin)

        con.execute(stmt)
        con.commit()
    except Exception as ex:
        print(ex)

def createAccount(key, secret, baseCurrency):
    con = sl.connect('./db/mydb.db')
    cur = con.cursor()

    stmt = """INSERT INTO Account (key, secret, currency) VALUES ("%s", '%s', '%s')""" %(key, secret, baseCurrency)
    try:
        con.execute(stmt)
        con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()