
import requests
import json
import pymysql
import time, datetime

url = 'http://127.0.0.1:9902'

data = '{"id":1,"method":"getwork","jsonrpc":"2.0","params":{"spent":"1pdr1knaaa4fzr846v89g3q2tzb8pbvbavbbft8xppkky0mqnmsq8gn5y","privkey":"ceae964a1119f110b0cff3614426dd692f8467a95cc2c276e523efc63c5e5031"}}'

response = requests.post(url, data=data)
result = json.loads(response.text)
print result

#data = '{"id":2,"method":"submitwork","jsonrpc":"2.0","params":{"data":"01000100502fae5b4624cce135b573bfc5d59315b7f779d7baf9c87db7ddb4d176d427a8e948e77e43000000000000000000000000000000000000000000000000000000000000000000011acfff020000000000000000000000000000000000000000000000000000000000","spent":"1dj5qcjst7eh4tems36n1m500hhyba3vx436t4a8hgdm7r7jrdbf2yqp9","privkey":"41a9f94395ced97d5066e2d099df4f1e2bd96057f9c38e8ea3f8a02eccd0a98e"}}'
#response = requests.post(url, data=data)
#result = json.loads(response.text)
#print result