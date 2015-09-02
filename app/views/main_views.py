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

@app.route('/', methods=['GET'])
def index_page():
    return flask.render_template('index_page.html')

@app.route('/redis/<redis_md5>.html', methods=['GET'])
def redis_monitor_page(redis_md5):
    return flask.render_template('redis_monitor_page.html', redis_md5 = redis_md5)


@app.route('/redis_information.json', methods=['GET', 'POST'])
def get_redis_paramter():
    try:
        host = RequestUtil.get_parameter(request, 'host', '127.0.0.1')
        port = int(RequestUtil.get_parameter(request, 'port', '6379'))
        password = RequestUtil.get_parameter(request, 'password', '')
        rst = RedisMonitor().get_info(host = host, port = port, password = password)
    except:
        rst = {'success': 0, 'data': ''}
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