#coding=utf-8
'''
Created on 2015年6月16日

@author: hzwangzhiwei
'''
from app import app, config
import flask
import redis
from app.utils import RequestUtil, OtherUtil
from flask.globals import request
import time

@app.route('/', methods=['GET'])
def index_page():
    redis = config.monitor_redis
    return flask.render_template('index_page.html', redis = redis)


@app.route('/<redis_index>.html', methods=['GET'])
def monitor_page(redis_index):
    try:
        redis_info = config.monitor_redis[int(redis_index)]
        redis_info['RD_INDEX'] = int(redis_index)
    except:
        redis_info = None
    if redis_info:
        redis = config.monitor_redis
        return flask.render_template('monitor_page.html', redis_info = redis_info, redis = redis)
    return flask.render_template('tip.html', tip = u'访问的redis不存在！', url = '/', text = u'返回首页！') 


@app.route('/redis_information.json', methods=['GET', 'POST'])
def get_redis_paramter():
    rst = {}
    
    redis_index = RequestUtil.get_parameter(request, 'id', '0')
    try:
        start = time.time()
        redis_info = config.monitor_redis[int(redis_index)]
        r = redis.Redis(host = redis_info['RD_HOST'], port = redis_info['RD_PORT'], password = redis_info['RD_PSW'], db = 0)
        info = r.info()
        end = time.time();
        info['get_time'] = end - start
        
        rst['success'] = 1
        rst['data'] = info
    except:
        redis_info = None
        rst['success'] = 0
        rst['data'] = 'error'
    return OtherUtil.object_2_dict(rst)

#定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return '404'

@app.errorhandler(502)
def server_502_error(error):
    return '502'

@app.route('/not_allow', methods=['GET'])
def deny(error):
    return 'You IP address is not in white list...'