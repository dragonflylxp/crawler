# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbabetItem(scrapy.Item):
    # define the fields for your item here like:
    RuleType = scrapy.Field()  #盘口类型 
    TeamName = scrapy.Field()  #球队名称
    BackOdds = scrapy.Field()  #赔率
     
   
