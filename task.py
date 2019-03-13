
import requests
import json
import pymysql
import time, datetime
from decimal import Decimal

url = 'http://127.0.0.1:9904'
#url = 'http://127.0.0.1:9904'
connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="bigbang")

def ExecSql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception, e:
        print e
        return 0

def InsertBlock(block_hash,sql):
    res = IsHaveHash(block_hash)
    if res == None:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    else:
        return res[0]
    

def InsertTx(block_id,tx):
    with connection.cursor() as cursor:
        sql = 'SELECT id from tx where txid = "%s"' % tx["txid"]
        cursor.execute(sql)
        connection.commit()
        res = cursor.fetchone()
        if res != None:
            return
        in_money = 0
        sendform = ""
        for vin in tx["vin"]:
            sql = "select id,amount,`to` from tx where txid = '%s' and n = %d" % (vin["txid"],vin["vout"])
            print sql
            cursor.execute(sql)
            res = cursor.fetchone()
            in_money = in_money + res[1]
            sendform = res[2]
            sql = "update tx set spend_txid = '%s' where id = %d" % (tx["txid"],res[0])
            cursor.execute(sql)
    
        sql = "insert tx(block_id,txid,form,`to`,amount,free,type,lock_until,n)values(%d,'%s','%s','%s',%s,%s,'%s',%d,0)" \
            % (block_id,tx["txid"], sendform,tx["sendto"],tx["amount"],tx["txfee"],tx["type"],tx["lockuntil"])
        cursor.execute(sql)
    
        if in_money > tx["amount"] + tx["txfee"]:
            amount = in_money - Decimal(tx["amount"] + tx["txfee"])
            sql = "insert tx(block_id,txid,form,`to`,amount,free,type,lock_until,n)values(%d,'%s','%s','%s',%s,%s,'%s',%d,1)" \
                % (block_id,tx["txid"],sendform,sendform,amount,0,tx["type"],0)
            cursor.execute(sql)
        connection.commit() 
    
def GetTask():
    with connection.cursor() as cursor:
        sql = 'SELECT id,block_hash from task where is_ok = 0 limit 1'
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchone()


def SbumitTask(taskid):
    with connection.cursor() as cursor:
        sql = 'update task set is_ok = 1 where id = %s' % taskid
        cursor.execute(sql)
        connection.commit()

def IsHaveHash(block_hash):
    with connection.cursor() as cursor:
        sql = 'select id from block where hash = "%s"' % block_hash
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchone()
        
def GetDelTask(height):
    task_del = []
    with connection.cursor() as cursor:
        sql = 'select hash from block where is_useful = 1 and height > %s'
        cursor.execute(sql,height)
        connection.commit()
        res = cursor.fetchall()
        for obj in res:
            task_del.append(obj[0])
    return task_del

def ExecDelTask(block_id):
    with connection.cursor() as cursor:
        sql = 'update block set is_useful = 0 where id = %s'
        cursor.execute(sql,block_id)
        sql = 'update tx set spend_txid = null where block_id = %s'
        cursor.execute(sql,block_id)
        connection.commit()

def HaveBlock(block_hash):
    pass

def ExecTask(block_hash):
    task_add = []
    task_del = []
    while True:
        db_res = IsHaveHash(block_hash)
        if db_res == None:
            data = '{"id":1,"method":"getblockdetail","jsonrpc":"2.0","params":{"block":"%s"}}' % block_hash    
            response = requests.post(url, data=data)
            res = json.loads(response.text)
            task_add.append(res)
            if res["result"]["height"] == 0:
                task_del = GetDelTask(0)
                break
            block_hash = res["result"]["hashPrev"]            
        else:
            task_del = GetDelTask(db_res[0])
            break

    task_add.reverse()
    task_del.reverse()

    for obj in task_del:
        ExecDelTask(obj)
    for res in task_add:
        obj = res["result"]
        reward_address = obj["txmint"]["sendto"]
        reward_money = obj["txmint"]["amount"]

        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj["time"]))
        sql = "insert block(hash,prev_hash,fork_hash,time,height,type,reward_address,reward_money)" \
                "values('%s','%s','%s','%s',%d,'%s','%s',%s)" \
                % (obj["hash"],obj["hashPrev"],obj["fork"], t,obj["height"],obj["type"],reward_address,reward_money)
        block_id = InsertBlock(obj["hash"],sql)
        InsertTx(block_id,obj["txmint"])
        for tx in obj["tx"]:
            InsertTx(block_id,tx)

if __name__ == '__main__':
    while True:
        rest = GetTask()
        if rest == None:
            time.sleep(3)
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"wait task..."
        else:
            print "exec task",rest
            ExecTask(rest[1])
            SbumitTask(rest[0])