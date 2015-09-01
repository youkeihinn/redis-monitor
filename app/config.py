#coding=utf-8
'''
Created on 2015年8月31日
安装配置
@author: hzwangzhiwei
'''

#需要被监控的redis服务器
monitor_redis = [{
    'RD_NAME': u'开发服务器',
    'RD_HOST': '10.246.14.121',
    'RD_PORT': 6379,
    'RD_PSW': None,
    'RD_CHARSET': 'utf8',
}, {
    'RD_NAME': u'生产服务器',
    'RD_HOST': '10.246.13.189',
    'RD_PORT': 6379,
    'RD_PSW': None,
    'RD_CHARSET': 'utf8',
}]