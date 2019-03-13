#!/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'shang'

import requests
import json
import pymysql
import time, datetime
from decimal import Decimal

connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="WhiteList")

def ExecSql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception, e:
        print(e)
        return 0

def GetTask(addr):
    with connection.cursor() as cursor:
        sql = "SELECT * from log where addr = '%s'" % addr
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchone()


import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
r.flushall()  

r.setex('name', value='liaogx', time=20)