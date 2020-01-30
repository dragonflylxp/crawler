#!/usr/bin/env python
# encoding: utf-8
"""
 * @author: cz
 * @description: 
"""
import logging

import redis
import requests
from apscheduler.schedulers.background import BackgroundScheduler


class ZhimaProxyScheduler(object):
    """
    芝麻代理后台任务,后动自动运行捉取动态代理IP存放到redis
    """

    def __init__(self,cron,url,host,port,password,key):
        self.cron=cron
        self.url = url
        self.scheduler = BackgroundScheduler()
        self.redisClient = redis.Redis(host=host, port=port, password=password, db=0)
        self.key = key

    @classmethod
    def from_crawler(cls, crawler):
        """
        Scrapy会先通过getattr判断我们是否自定义了from_crawler,有则调它来完
        成实例化
        """
        cron = crawler.settings.get('PROXY_CRON')
        url = crawler.settings.get('PROXY_URL')
        host = crawler.settings.get('REDIS_HOST')
        port = crawler.settings.get('REDIS_PORT')
        password = crawler.settings.get('REDIS_PASSWORD')
        key = crawler.settings.get('REDIS_PROXIES_KEY')
        return cls(cron,url,host,port,password,key)

    def _run(self):
        try:
            repsone = requests.get(self.url)
            str = repsone.text.replace("\r\n", ",")
            logging.info("获取到代理ip池:%s" %str)
            self.redisClient.set(self.key,str)
        except Exception as ex:
            logging.error("获取代理ip异常:%s" %ex)
            self.redisClient.set(self.key,"")


    def open_spider(self,spider):
        """
        爬虫刚启动时执行一次
        """
        self._run()
        # 设置为后台更新任务
        self.scheduler.add_job(self._run, 'cron', second =self.cron)
        #self.scheduler.add_job(self._run, 'cron', minutes =self.cron)
        self.scheduler.start()


    def close_spider(self,spider):
        """
        爬虫关闭时执行一次
        """
        self.scheduler.shutdown()

    def process_item(self, item, spider):
         pass
