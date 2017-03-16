# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class WeixinPipeline(object):
    def __init__(self):
        self.fp = open('wexin.json','wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.fp.write(line.encode('utf-8'))

    def __del__(self):
        self.fp.close()  
          
