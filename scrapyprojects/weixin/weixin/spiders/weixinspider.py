# -*- coding: utf-8 -*-
import scrapy
from weixin.items import WeixinItem 


class WeixinspiderSpider(scrapy.Spider):
    name = "weixinspider"
    allowed_domains = ["weixin.sogou.com"]
    start_urls = ['http://weixin.sogou.com']

    def parse(self, response):
        item = WeixinItem()
        item['title'] = response.xpath('//h3/a/text()').extract()
        item['abstract'] = response.xpath('//p/text()').extract()
        return item
