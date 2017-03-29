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
    Abbr = scrapy.Field()
    City = scrapy.Field()
    CityEn = scrapy.Field()
    Code = scrapy.Field()
    Conference = scrapy.Field()
    DisplayAbbr = scrapy.Field()
    DisplayConference = scrapy.Field()
    TeamID = scrapy.Field()
    IsAllStarTeam = scrapy.Field()
    IsLeagueTeam = scrapy.Field()
    LeagueID = scrapy.Field()
    Name = scrapy.Field()
    NameEn = scrapy.Field()
    Logo = scrapy.Field()
    ConfRank = scrapy.Field()
    HeadCoach= scrapy.Field()
