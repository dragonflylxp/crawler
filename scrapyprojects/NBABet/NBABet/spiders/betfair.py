# -*- coding: utf-8 -*-
import scrapy


class BetfairSpider(scrapy.Spider):
    name = "betfair"
    allowed_domains = ["www.betfair.com"]
    start_urls = ['http://www.betfair.com/']

    def parse(self, response):
        pass
