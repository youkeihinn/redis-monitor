#coding=utf-8
'''
Created on 2015年9月2日

@author: hzwangzhiwei
'''
from app.wraps.singleton_wrap import singleton
import hashlib
import time
import redis
import traceback



@singleton
class RedisMonitor(object):
    '''
    classdocs
    '''
    def __init__(self, timeout = 1):
        '''
        Constructor
        '''
        self.timeout = timeout #数据过期时间
        self.servers = {}
        self.redis_requesting = False #全局控制请求，尽量减少请求数
        
    def _md5(self, s):
        '''
        md5
        '''
        m = hashlib.md5()   
        m.update(s)
        return m.hexdigest()
    
    def ping(self, host, port, password, charset = 'utf8'):
        if host and port:
            redis_rst = {}
            #需要重新请求获得数据
            try:
                r = redis.Redis(host = host, port = port, password = password, db = 0)
                r.info()
                
                redis_rst['success'] = 1
                redis_rst['data'] = 'ping success'
            except:
                redis_rst['success'] = 0
                redis_rst['data'] = 'ping error'
            
            return redis_rst
        else:
            #如果host，port非法，则直接返回错误
            return {'success': 0, 'data': 'parameter error'}
    
    def new_request(self, key, host, port, password, charset = 'utf8'):
        redis_rst = {}
        #需要重新请求获得数据
        self.redis_requesting = True
        try:
            start = time.time()
            
            r = redis.Redis(host = host, port = port, password = password, db = 0)
            info = r.info()
            end = time.time();
            info['get_time'] = end - start
            
            redis_rst['success'] = 1
            redis_rst['data'] = info
        except:
            redis_rst['success'] = 0
            redis_rst['data'] = 'error'
        #将获取的redis信息保存到内存中，缓存起来
        self.servers[key] = {}
        self.servers[key]['time'] = time.time() #更新时间
        self.servers[key]['info'] = redis_rst
        self.redis_requesting = False
        
        return redis_rst
    
    def get_info(self, host, port, password, charset = 'utf8'):
        redis_rst = {}
        if host and port:
            key = self._md5(host + str(port))
            #小于timeout，不用重新连接redis获取信息，直接拉缓存数据
            if key in self.servers.keys():
                if self.redis_requesting:
                    redis_rst = self.servers[key]['info']
                else:
                    if time.time() - self.servers[key]['time'] < self.timeout:
                        redis_rst = self.servers[key]['info']
                    else:
                        #已经过期
                        redis_rst = self.new_request(key, host, port, password, charset)
            else:
                if self.redis_requesting:
                    redis_rst = {'success': 0, 'data': 'requesting'}
                else:
                    #第一次请求数据
                    redis_rst = self.new_request(key, host, port, password, charset)
                
        else:
            #如果host，port非法，则直接返回错误
            redis_rst = {'success': 0, 'data': 'parameter error'}
        return redis_rst