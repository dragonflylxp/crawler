# -*- coding: utf-8 -*-
import scrapy
import ujson
from NBA.items import TeamItem

teamlist_url = 'http://china.nba.com/static/data/league/divisionteamlist.json'
teaminfo_url = 'http://china.nba.com/static/data/team/standing_{}.json'
teamlogo_url = 'http://china.nba.com/media/img/teams/logos/{}_logo.svg' 

class TeaminfoSpider(scrapy.Spider):
    name = "teaminfo"
    allowed_domains = ["china.nba.com"]
    start_urls = [teamlist_url]

    def parse(self, response):
        try:
            teamindex = ujson.loads(response.body)
            groups = teamindex.get("payload",{}).get("listGroups",[]) 
            for group in groups:
                teams = group.get("teams",[])
                for team in teams:
                    url = teaminfo_url.format(team.get('profile',{}).get('code',''))
                    yield scrapy.Request(url,callback=self.teaminfo)
        except Exception as ex:
            print(ex)

    def teaminfo(self, response):
        try:
            teaminfo = ujson.loads(response.body)  
            team = teaminfo.get('payload',{}).get('team',{}) 
            league = teaminfo.get('payload',{}).get('league',{}) 
            season = teaminfo.get('payload',{}).get('season',{}) 

            #team-profile
            profile = team.get('profile',{})
            item = TeamItem()
            item['abbr'] = profile.get('abbr','') 
            item['city'] = profile.get('city','') 
            item['cityEn'] = profile.get('cityEn','') 
            item['code'] = profile.get('code','') 
            item['conference'] = profile.get('conference','') 
            item['displayAbbr'] = profile.get('displayAbbr','') 
            item['displayConference'] = profile.get('displayConference','') 
            item['teamId'] = profile.get('id','') 
            item['isAllStarTeam'] = profile.get('isAllStarTeam','') 
            item['isLeagueTeam'] = profile.get('isLeagueTeam','') 
            item['leagueId'] = profile.get('leagueId','') 
            item['name'] = profile.get('name','') 
            item['nameEn'] = profile.get('nameEn','') 
            item['logo'] = teamlogo_url.format(profile.get('abbr','')) 
            return item
        except Exception as ex:
            print(ex)
            
            
