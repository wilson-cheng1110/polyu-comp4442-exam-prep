import time
import mysql.connector
import json
import random

def db_connection():
    mydb = mysql.connector.connect( host = 'database-1.cti2wk8aib5l.us-east-1.rds.amazonaws.com',
    user = 'admin',
    port = '3306',
    database = 'lab6',
    passwd = '12345678',
    autocommit = True)
    return mydb

mydb = db_connection()
cur = mydb.cursor()

def genData():
    number=15 + 5*random.randint(1,10)
    Time = int(time.time())
    data = {}
    data['time'] = Time
    data['number'] = number
    return data

def execute():
    data = genData()
    sql = "insert into Monitor(num,ctime) values ({0},{1})".format(data['number'],data['time'])
    print(sql)
    ret = cur.execute(sql)

while True:   
    execute()
    time.sleep(1)