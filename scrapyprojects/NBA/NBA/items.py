# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TeamItem(scrapy.Item):
    #profile
    abbr = scrapy.Field()
    city = scrapy.Field()
    cityEn = scrapy.Field()
    code = scrapy.Field()
    conference = scrapy.Field()
    displayAbbr = scrapy.Field()
    displayConference = scrapy.Field()
    teamId = scrapy.Field()
    isAllStarTeam = scrapy.Field()
    isLeagueTeam = scrapy.Field()
    leagueId = scrapy.Field()
    name = scrapy.Field()
    nameEn = scrapy.Field()
    logo = scrapy.Field()

    #standings
    #rank
    #coach

    
