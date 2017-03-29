# coding: utf-8

import redis
import memcache
import ujson
from pymongo import *

from connection import PoolManager

configs = {
            'database':{
                'mysql':{
                    "crazy_bet":{
                        "host":"10.0.1.27",
                        "port": 3306,
                        "db":"crazy_bet",
                        "charset":"utf8",
                        "user":"crazy_bet",
                        "passwd":"crazy_bet",
                        "cached":12
                        }
                },
                "redis": {
                    "main": {
                        "host": "192.168.41.76",
                        "port": 6379,
                        "db": 0,
                        "max_connections": 8
                        },
                    "msgbus": {
                        "host": "192.168.41.76",
                        "port": 6379,
                        "db": 8,
                        "max_connections": 8
                        }
                },
                "mongodb": {
                    "crazy_bet": {
                        "host": "mongodb://crazy_bet_rw:crazy_bet_rw@192.168.41.54:27017/crazy_bet",
                        "maxPoolSize":100,
                        "socketKeepAlive": True
                    }
                }

            }

        }

PoolManager.set_up(configs['database']['mysql'])

redis_pools = {}
mongodb_pools = {}


def get_redis(dbid, standalone=False):
    conf = configs['redis'][dbid].copy()
    if standalone:
        conf.pop('max_connections', None)
        return redis.Redis(**conf)
    pool = redis_pools.get(dbid)
    if not pool:
        conf.setdefault('max_connections', 8)
        pool = redis.ConnectionPool(**conf)
        redis_pools[dbid] = pool
    return redis.Redis(connection_pool=pool)


########################################


def get_mysql(dbid, standalone=False):
    return PoolManager.instance().get_a_pool(dbid).get_conn()


########################################


class MemCache(object):

    def __init__(self, *args, **kwargs):
        self._client = memcache.Client(*args, **kwargs)

    def __del__(self):
        self.close()

    def __getattr__(self, name):
        return getattr(self._client, name)

    def close(self):
        self._client.disconnect_all()


def get_memcache(dbid):
    # todo: memcache使用连接池
    return MemCache(**configs['memcache'][dbid])

# mongodb
def get_mongo(dbid):
    client_pool = mongodb_pools.get(dbid)
    if not client_pool:
        client_pool = MongoClient(**configs['database']['mongodb'][dbid])
        mongodb_pools[dbid] = client_pool
    return client_pool


def Cache(redis_key, expire=15 * 60, use_cache=True):
    """统一缓存处理
    """
    def deco(func):
        def wrapper(self, *args, **kwargs):
            if len(args) >= 1:
                REDIS_KEY = redis_key.format(*args)
            else:
                REDIS_KEY = redis_key
            redis_conn = get_redis("main")
            cache_str = redis_conn.get(REDIS_KEY)
            if cache_str and use_cache and config_cache:
                cache = ujson.loads(cache_str)
                return cache

            cache = func(self, *args, **kwargs)
            cache_str = ujson.dumps(cache)
            redis_conn.set(REDIS_KEY, cache_str, expire)

            return cache
        return wrapper
    return deco
