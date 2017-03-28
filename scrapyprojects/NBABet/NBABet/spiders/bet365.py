# -*- coding: utf-8 -*-
import scrapy
from NBABet.items import NbabetItem



class Bet365Spider(scrapy.Spider):
    name = "bet365"
    allowed_domains = ["www.38-365365.com"]
    start_urls = ['https://www.38-365365.com/#/AC/B18/C20483712/D1/E29618674/F2/I0/',
                  'https://www.38-365365.com/#/AC/B18/C20483712/D1/E30965855/F2/I0/']

    def parse(self, response):
        pass
        """
        item = NbabetItem()
        item['RuleType'] = response.xpath().extract() 
        item['TeamName'] = response.xpath().extract() 
        item['BackOdds'] = response.xpath().extract()
        return item
        """
        
