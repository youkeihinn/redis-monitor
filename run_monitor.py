#coding=utf-8
'''
Created on 2014年7月19日
一个flask 的sample
@contact: http://www.atool.org
'''


from app import app
if __name__ == '__main__':
    app.run('0.0.0.0', 7259, debug = True,  threaded = True)

