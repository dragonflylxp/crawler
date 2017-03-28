# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from NBA.items import TeamItem

class NbaPipeline(object):
    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):
        print(item)
        return item

    def close_spider(self,spider):
        pass
