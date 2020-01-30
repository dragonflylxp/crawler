'''
@Author: kaybinwong
@Since: 1.0.0
@Date: 2020-01-10
'''
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GoodsItem(scrapy.Item):
    """
    商品数据模型
    """
    amzUrl = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    rank = scrapy.Field()
    reviewStars = scrapy.Field()
    reviewRating = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    category3 = scrapy.Field()
    category4 = scrapy.Field()
    #category = scrapy.Field()
    categoryPath = scrapy.Field()
    asin = scrapy.Field()
    price = scrapy.Field()
    amzProprietary = scrapy.Field()
    gradeAvg = scrapy.Field()
    gradeTimes = scrapy.Field()
    commentTimes = scrapy.Field()
    description = scrapy.Field()
    pics = scrapy.Field()
    #sold = scrapy.Field()
    #ship = scrapy.Field()
    merchantInfo = scrapy.Field()
    overName = scrapy.Field()
