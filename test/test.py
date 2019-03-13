import time
import pymysql
import requests
import json
import pymysql
import time, datetime
import os
#sudo  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pymysql
#sudo  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests

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

def GetA():
    with connection.cursor() as cursor:
        sql = 'SELECT max(a) as a from block_test'
        cursor.execute(sql)
        connection.commit()
        return cursor.fetchone()

url = 'http://127.0.0.1:9902'
height = 1
t = 0
a = GetA()[0] + 1
while  True:
    data = '{"id":37,"method":"getblockhash","jsonrpc":"2.0","params":{"height":%s}}' % height
    response = requests.post(url, data=data)
    res = json.loads(response.text)
    print res
    block_hash = res["result"][0]

    data = '{"id":1,"method":"getblockdetail","jsonrpc":"2.0","params":{"block":"%s"}}' % block_hash
    response = requests.post(url, data=data)
    res = json.loads(response.text)
    sql = "INSERT block_test(height,bits,t,`hash`,tl,a) VALUES(%s,%s,%s,'%s',%s,%s);" % (height,res["result"]["bits"],res["result"]["time"], block_hash,res["result"]["time"] - t,a)
    if t > 0:
        ExecSql(sql)
    height = height + 1
    t = res["result"]["time"]
    print height,t