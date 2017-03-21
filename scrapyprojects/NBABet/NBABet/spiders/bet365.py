# -*- coding: utf-8 -*-
import scrapy


class Bet365Spider(scrapy.Spider):
    name = "bet365"
    allowed_domains = ["www.38-365365.com"]
    start_urls = ['http://www.38-365365.com/']

    def parse(self, response):
        pass
