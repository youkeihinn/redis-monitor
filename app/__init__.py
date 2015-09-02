#coding=utf-8
'''
Created on 2015年6月16日

@author: hzwangzhiwei
'''
from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_session_key_redis_monitor'

from app.views import main_views