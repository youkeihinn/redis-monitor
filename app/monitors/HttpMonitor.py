#coding=utf-8
'''
Created on 2015年9月2日

@author: hzwangzhiwei
'''
import hashlib
import time
import requests

class HttpMonitor(object):
    '''
    classdocs
    '''


    def __init__(self, timeout = 1):
        '''
        Constructor
        '''
        self.timeout = timeout #数据过期时间
        self.servers = {}
        
    
    def _md5(self, s):
        '''
        md5
        '''
        m = hashlib.md5()   
        m.update(s)
        return m.hexdigest().upper()
    
    #暂时不带参数
    def get_info(self, url, method = "GET", params = {}):
        method = method.upper()
        if url and method in ['GET', 'POST', 'PUT', 'DELETE']:
            key = self._md5(url + method)
            if key in self.servers.keys() and (time.time() - self.servers[key]['time'] < self.timeout):
                return self.servers[key]['info']
            else:
                http_rst = {}
                #需要重新请求获得数据
                try:
                    start = time.time()
                    if method == "POST":
                        r = requests.post(url, params = params)
                    elif method == "GET":
                        r = requests.get(url, params = params)
                    elif method == "PUT":
                        r = requests.put(url, params = params)
                    elif method == "DELETE":
                        r = requests.delete(url, params = params)
                    
                    end = time.time();
                    info = {}
                    info['get_time'] = end - start
                    info['encoding'] = r.encoding
                    info['status_code'] = r.status_code
                    info['headers'] = r.headers
                    
                    http_rst['success'] = 1
                    http_rst['data'] = info
                except:
                    #连接失败
                    http_rst['success'] = 0
                    http_rst['data'] = 'error'
                
                #将获取的redis信息保存到内存中，缓存起来
                self.servers[key] = {}
                self.servers[key]['time'] = time.time() #更新时间
                self.servers[key]['info'] = http_rst
                
                return http_rst
        else:
            #如果host，port非法，则直接返回错误
            return {'success': 0, 'data': 'parameter error'}