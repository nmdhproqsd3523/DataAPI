#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import pymysql
import json
import requests
#blocknotify=python /home/shang/DataAPI/sync-data/block_notice.py

connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", db="bigbang")

for num in range(2, len(sys.argv)):
    with connection.cursor() as cursor :
        cursor.execute("select * from Task where is_ok = 0")
        connection.commit()
        if cursor.fetchone() == None:
            forkid = sys.argv[1]
            block_hash = sys.argv[num]
            sql = "insert Task(forkid,block_hash) values('%s','%s')" % (forkid,block_hash)
            cursor.execute(sql)
            connection.commit()