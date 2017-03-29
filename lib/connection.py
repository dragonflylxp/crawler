#!/usr/bin/python
#coding=utf-8
# author Rowland
# edit 2014-03-19 14:16:13
#MySQLdb, DButils#
import os, MySQLdb, MySQLdb.connections, threading, redis, time
from DBUtils import PooledDB
import six


class NoConnections(Exception):
    pass


class NoPools(Exception):
    pass


class CannotInitException(Exception):
    pass


class ConnectionPool(object):
    '''
    数据库连接池。这个类只提供连接，使用者需要自己手动关闭连接
    '''

    def __init__(self, _host, _port, _db, _charset, _user, _passwd, _cached):
        self.check_conn(_host, _port, _db, _user, _passwd)
        self.pool = PooledDB.PooledDB(MySQLdb, mincached=_cached,
                                      maxcached=_cached + 10, host=_host, user=_user,
                                      passwd=_passwd, db=_db, charset=_charset)

    def check_conn(self, _host, _port, _db, _user, _passwd):
        c = MySQLdb.connect(host=_host,port=_port, db=_db, user=_user, passwd=_passwd)
        c.close()

    def get_conn(self, block=False, timeout=-1):
        '''
        取得一个数据库连接, block参数为True且连接池无cache连接会等待直到超时或有
        可用cached连接，当timeout为负数且block为True的时候，为无限等待直到有可用连接
        '''
        begin = time.time()
        while block and self.pool._maxcached <= self.pool._connections:
            if 0 <= timeout < time.time() - begin:
                raise NoConnections
        return self.pool.connection()

    def shutdown(self):
        '''
        关闭所有连接
        '''
        for conn in self.pool:
            conn.close()


class PoolManager(object):
    _instance_lock = threading.Lock()
    _cfg = {}
    _pools = {}

    @classmethod
    def set_up(cls, cfg):
        PoolManager._cfg = cfg
        for db, cfg in six.iteritems(PoolManager._cfg):
            _host = cfg.get("host")
            _port = cfg.get("port")
            _db = cfg.get("db")
            _charset = cfg.get("charset")
            _user = cfg.get("user")
            _passwd = cfg.get("passwd")
            _cached = cfg.get("cached")
            pool = ConnectionPool(_host, _port, _db, _charset, _user, _passwd, _cached)
            PoolManager._pools[db] = pool

    def __init__(self):
        raise CannotInitException('cannot initialize a singleton class')

    @staticmethod
    def instance():
        if not hasattr(PoolManager, "_instance"):
            with PoolManager._instance_lock:
                PoolManager._instance = object.__new__(PoolManager)
        if not PoolManager._pools:
            raise NoPools('No connection pool hold, plz check your connection configurations')
        return PoolManager._instance

    @staticmethod
    def get_a_pool(db):
        return PoolManager._pools.get(db)


