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
        print(e)
        return 0

#getblockcount
#getblockhash

data = '{"id":1,"method":"getblockcount","jsonrpc":"2.0","params":{}}'
response = requests.post(url, data=data)
result = json.loads(response.text)

data = '{"id":1,"method":"getblockhash","jsonrpc":"2.0","params":{"height":%d}}' % (result["result"] - 1)

response = requests.post(url, data=data)
result = json.loads(response.text)
block_hash = result["result"][0]

while True:
    
    data = '{"id":1,"method":"getblock","jsonrpc":"2.0","params":{"block":"%s"}}' % block_hash
    response = requests.post(url, data=data)
    result = json.loads(response.text)
    
    print(result)
#curl -d '{"id":37,"method":"getblockhash","jsonrpc":"2.0","params":{"height":0}}' http://127.0.0.1:9902
