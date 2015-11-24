#coding=utf-8
'''
Created on 2014年7月19日
@contact: http://www.atool.org
'''


from app import app
import os
from app.dbs.sqlite_utils import sqlite_info
from app.dbs import redisinfo_dbs

if __name__ == '__main__':
    #init tables
    if not os.path.exists(sqlite_info.get('DB', 'redis_info.db')):
        redisinfo_dbs.create_tables()
    
    app.run('0.0.0.0', 7259, debug = True,  threaded = True)

