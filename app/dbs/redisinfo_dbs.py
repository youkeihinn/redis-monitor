#coding=utf-8
'''
Created on 2015年11月24日

@author: hzwangzhiwei
'''
from app.dbs.sqlite_utils import SqliteHandler
from app.utils import StringUtil, DateUtil


def get_all_redis():
    '''
    info: 获取数据库中所有的redis信息
    '''
    sql = "select * from redis_info order by add_time desc;"
    params = ()
    return SqliteHandler().exec_select(sql, params)


def add_redis(host, port, psw, email):
    '''
    info: 添加一个redis信息到数据库
    '''
    add_time = DateUtil.now_datetime()
    md5 = StringUtil.md5(host + str(port))
    r = get_redis(md5)
    if r:
        #存在，update
        sql = "update redis_info set redis_host = ?, redis_port = ?, redis_pass = ?, email = ?, add_time = ? where md5 = ?"
        params = (host, port, psw, email, add_time, md5)
        return SqliteHandler().exec_update(sql, params)
    else:
        sql = "insert into redis_info (redis_host, redis_port, redis_pass, email, add_time, md5) values (?, ?, ?, ?, ?, ?)"
        params = (host, port, psw, email, add_time, md5)
        return SqliteHandler().exec_insert(sql, params)
    

def delete_redis(md5):
    '''
    info: delete redis information from db
    '''
    sql = "delete from redis_info where md5 = ?"
    params = (md5, )
    return SqliteHandler().exec_update(sql, params)


def get_redis(md5):
    '''
    info: get one redis information
    '''
    sql = "select * from redis_info where md5 = ?"
    params = (md5, )
    return SqliteHandler().exec_select_one(sql, params)


def create_tables():
    '''
    info:创建表结构，第一次初始化的时候使用
    '''
    sql = ("create table redis_info("
           "redis_host varchar, "
           "redis_port varchar, "
           "redis_pass varchar, "
           "add_time varchar, "
           "email varchar, "
           "md5 varchar)")
    
    SqliteHandler().exec_sql(sql, ())
    
if __name__ == '__main__':
    create_tables()