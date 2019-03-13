#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import pymysql
import json
import requests 
from datetime import datetime, date
import time
import datetime

connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="bigbang")
reward_info = {}
dpos_info = {}

def UpdateVote(dpos_addr, client_addr,money):
    if dpos_addr in dpos_info and client_addr in dpos_info[dpos_addr]:
        dpos_info[dpos_addr][client_addr] += money
    else:
        dpos_info[dpos_addr] = {}
        dpos_info[dpos_addr][client_addr] = money

def UpdateReward(dpos_addr,reward):
    total = 0
    if dpos_addr in dpos_info:
        for client_addr in dpos_info[dpos_addr]:
            total += dpos_info[dpos_addr][client_addr]
        for client_addr in dpos_info[dpos_addr]:
            if dpos_addr in reward_info and client_addr in reward_info[dpos_addr]:
                reward_info[dpos_addr][client_addr] += reward * dpos_info[dpos_addr][client_addr] / total
            else:
                reward_info[dpos_addr] = {}
                reward_info[dpos_addr][client_addr] = reward * dpos_info[dpos_addr][client_addr] / total

def Init(payment_date):
    sql = "SELECT dpos_addr,client_addr,audit_money FROM DposState where audit_date = %s" % payment_date
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    for row in rows:
        dpos_info[row[0]][row[1]] = row[2]
    return True

def Run(begin_time,end_time):
    dpos_info = {}
    cursor = connection.cursor()
    sql = "SELECT `hash`,reward_address,reward_money FROM `Block` where is_useful = 1 and time >= %d and time < %d" % (begin_time,end_time)
    print sql
    cursor.execute(sql)
    blocks = cursor.fetchall()
    for block in blocks:
        sql = "SELECT dpos_in,client_in,dpos_out,client_out,amount,free FROM `Tx` where block_hash = '%s' and (dpos_in != '' or dpos_out != '')" % block[0]
        cursor.execute(sql)
        txs = cursor.fetchall()
        for tx in txs:
            if tx[0] != "":
                UpdateVote(tx[0],tx[1],tx[4])
            if tx[1] != "":
                UpdateVote(tx[2],tx[3],-tx[4]-tx[5])
        UpdateReward(block[1],block[2])
    
def Complete(payment_date):
    cursor = connection.cursor()
    for dpos_addr in dpos_info:
        for client_addr in dpos_info[dpos_addr]:
            sql = "insert DposState(dpos_addr,client_addr,audit_money,audit_date) values('%s','%s','%s','%s')" % (dpos_addr,client_addr,dpos_info[dpos_addr][client_addr],payment_date)
            cursor.execute(sql)
    
    for dpos_addr in reward_info:
        for client_addr in reward_info[dpos_addr]:
            sql = "insert DposPayment(dpos_addr,client_addr,payment_money,payment_date) values('%s','%s','%s','%s')" % (dpos_addr,client_addr,reward_info[dpos_addr][client_addr],payment_date)
            cursor.execute(sql)
    connection.commit()

def GetLastDate():
    with connection.cursor() as cursor:
        sql = 'SELECT audit_date FROM `DposState` ORDER BY id desc LIMIT 1'
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchone()

def GetLastRange(payment_date):
    payment_date_time = datetime.datetime.strptime(str(payment_date),'%Y-%m-%d')
    begin = int(time.mktime(payment_date_time.timetuple()))
    end = begin + 60 * 60 * 24
    return begin,end

if __name__ == '__main__':
    while True:
        localtime = time.localtime(time.time())
        payment_date = GetLastDate()
        if payment_date is None:
            payment_date = datetime.date(2020,3,10)
        else:
            payment_date = payment_date[0]
            payment_data = payment_date + datetime.timedelta(days=1)

        Init(payment_date)
        time_begin,time_end = GetLastRange(payment_date)
        Run(time_begin,time_end)
        Complete(payment_date)
        print time_begin,time_end
        sys.exit()
        if payment_date + datetime.timedelta(days=1) <  datetime.date.today() and localtime.tm_hour >= 1:
            Init(payment_date)
            time_begin,time_end = GetLastRange(payment_date)
            Run(time_begin,time_end)
            payment_data = payment_date + datetime.timedelta(days=1)
            Complete(payment_date)
        else:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"wait task 60s ..."
            time.sleep(60)