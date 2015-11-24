#coding=utf-8
'''
Created on 2015年6月16日

@author: hzwangzhiwei
'''
from app import app
import flask
from app.utils import RequestUtil, OtherUtil
from flask.globals import request
from app.monitors.RedisMonitor import RedisMonitor
from app.dbs import redisinfo_dbs

@app.route('/', methods=['GET'])
def index_page():
    redis_all = redisinfo_dbs.get_all_redis()
    return flask.render_template('index_page.html', redis_all = redis_all)

@app.route('/redis/<redis_md5>.html', methods=['GET'])
def redis_monitor_page(redis_md5):
    redis = redisinfo_dbs.get_redis(redis_md5)
    
    return flask.render_template('redis_monitor_page.html', redis = redis)


@app.route('/redis_information.json', methods=['GET', 'POST'])
def get_redis_paramter():
    try:
        redis_md5 = RequestUtil.get_parameter(request, 'md5', '')
        redis_info = redisinfo_dbs.get_redis(redis_md5)
        if redis_info:
            rst = RedisMonitor().get_info(host = redis_info['redis_host'], port = redis_info['redis_port'], password = redis_info['redis_pass'])
        else:
            rst = {'success': 0, 'data': 'not exist redis informations'}
    except:
        rst = {'success': 0, 'data': 'get redis realtime information error'}
    return OtherUtil.object_2_dict(rst)


@app.route('/api/ping', methods=['GET', 'POST'])
def redis_ping():
    try:
        host = RequestUtil.get_parameter(request, 'host', '')
        port = int(RequestUtil.get_parameter(request, 'port', '6379'))
        password = RequestUtil.get_parameter(request, 'password', '')
        rst = RedisMonitor().ping(host = host, port = port, password = password)
    except:
        rst = {'success': 0, 'data': 'ping error'}
    return OtherUtil.object_2_dict(rst)

@app.route('/api/add', methods=['GET', 'POST'])
def add_redis():
    redis_host = RequestUtil.get_parameter(request, 'host', '')
    redis_port = int(RequestUtil.get_parameter(request, 'port', '6379'))
    redis_pass = RequestUtil.get_parameter(request, 'password', '')
    email = RequestUtil.get_parameter(request, 'email', '')
    
    rid = redisinfo_dbs.add_redis(redis_host, redis_port, redis_pass, email)
    
    if rid:
        rst = {'success': 1, 'data': ''}
    else:
        rst = {'success': 0, 'data': 'add redis error'}
    return OtherUtil.object_2_dict(rst)


@app.route('/api/del', methods=['GET', 'POST'])
def del_redis():
    redis_md5 = RequestUtil.get_parameter(request, 'md5', '')
    rid = redisinfo_dbs.delete_redis(redis_md5)
    if rid:
        rst = {'success': 1, 'data': ''}
    else:
        rst = {'success': 0, 'data': 'del redis error'}
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