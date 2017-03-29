# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from NBA.items import TeamItem
from mongodao import MongoDataModel
import datetime

class NbaPipeline(object):
    def open_spider(self,spider):
        self.dao = MongoDataModel()

    def process_item(self, item, spider):
        doc = dict(item)
        doc['UpDateTime'] = datetime.datetime.now()
        SON = {'TeamID': doc['TeamID']}
        DOC = {'$set': doc,
               '$setOnInsert':{'AddDateTime':datetime.datetime.now()}}
        self.dao.update("t_basketballteams",SON,DOC,upsert=True)

    def close_spider(self,spider):
        pass
