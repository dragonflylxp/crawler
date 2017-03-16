# -*- coding: utf-8 -*-
import scrapy


class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["lagou.com"]
    start_urls = ['http://lagou.com/']
    start_urls = ['https://www.lagou.com/jobs/list_python?px=default&city=%E6%B7%B1%E5%9C%B3']

    def parse(self, response):
        pass
