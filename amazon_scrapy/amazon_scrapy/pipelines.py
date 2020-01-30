'''
@Author: kaybinwong
@Since: 1.0.0
@Date: 2020-01-10
'''
# -*- coding: utf-8 -*-

import json
import logging
import csv

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pika
from scrapy.exceptions import DropItem

class CSVPipeline(object):
    """
    负责把处理的item放到CSV中
    """
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.csv_file = None
        self.csv_writer = None

    @classmethod
    def from_crawler(cls, crawler):
        #csv_path = crawler.settings.get('CSV_PATH')
        csv_path = './amazon_bestseller.csv' 
        return cls(csv_path)

    def open_spider(self,spider):
        if self.csv_file is not None:
            self.csv_file.close()
            self.csv_file = None
        self.csv_file = open(self.csv_path, 'w', encoding='utf-8-sig')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["商品ASIN", "商品名称", "品牌商", "商品分类", "商品价格", "物流信息", "TOP100排名", "客户评价","客户评价数",  "商品图片",  "商品链接"])

    def close_spider(self,spider):
        self.csv_file.close()
        self.csv_file = None

    def process_item(self, item, spider):
        if item['name'] == "":
              raise DropItem("商品名称为空 %s" % item)
        else:
            logging.info("往CSV中存放item:%s" % json.dumps(item.__dict__))
            self.csv_writer.writerow([item["asin"], item["name"], item["brand"], item["categoryPath"], 
                                      item["price"], item["merchantInfo"], item["rank"], item["reviewStars"], 
                                      item["reviewRating"], item["pics"], item["amzUrl"]]) 

class RabbitMQPipeline(object):
    """
    负责把处理的item放到mq队列中
    """
    def __init__(self,host,port,virtual,user,password,queue,key):
        self.host=host
        self.port=port
        self.virtual=virtual
        self.user=user
        self.password=password
        self.queue = queue
        self.key = key

    @classmethod
    def from_crawler(cls, crawler):
        """
        Scrapy会先通过getattr判断我们是否自定义了from_crawler,有则调它来完
        成实例化
        """
        host = crawler.settings.get('RABBIT_MQ_HOST')
        port = crawler.settings.get('RABBIT_MQ_PORT')
        virtual = crawler.settings.get('RABBIT_MQ_VIRTUAL_HOST')
        user = crawler.settings.get('RABBIT_MQ_USER')
        password = crawler.settings.get('RABBIT_MQ_PASSWORD')
        queue = crawler.settings.get('RABBIT_MQ_QUEUE')
        key = crawler.settings.get('RABBIT_MQ_ROUTING_KEY')

        return cls(host,port,virtual,user,password,queue,key)

    def open_spider(self,spider):
        """
        爬虫刚启动时执行一次
        """
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                            virtual_host=self.virtual,
                                            credentials=credentials,
                                            heartbeat=0)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue,durable=True)


    def close_spider(self,spider):
        """
        爬虫关闭时执行一次
        """
        self.connection.close()


    def process_item(self, item, spider):
        if item['name'] == "":
              raise DropItem("商品名称为空 %s" % item)
        else:
            data = json.dumps(dict(item))
            logging.info("往MQ中存放item:%s" % data)
            self.channel.basic_publish(exchange='',
                routing_key=self.key,
                body=data,
                properties=pika.BasicProperties(content_type = 'application/json')
            )
