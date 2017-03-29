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
            standings = team.get('standings',{})
            coach = team.get('coach',{})
            item = TeamItem()
            item['Abbr'] = profile.get('abbr','')
            item['City'] = profile.get('city','')
            item['CityEn'] = profile.get('cityEn','')
            item['Code'] = profile.get('code','')
            item['Conference'] = profile.get('conference','')
            item['DisplayAbbr'] = profile.get('displayAbbr','')
            item['DisplayConference'] = profile.get('displayConference','')
            item['TeamID'] = profile.get('id','')
            item['IsAllStarTeam'] = profile.get('isAllStarTeam','')
            item['IsLeagueTeam'] = profile.get('isLeagueTeam','')
            item['LeagueID'] = profile.get('leagueId','')
            item['Name'] = profile.get('name','')
            item['NameEn'] = profile.get('nameEn','')
            item['Logo'] = teamlogo_url.format(profile.get('abbr',''))
            item['ConfRank'] = standings.get('confRank',-1)
            item['HeadCoach'] = coach.get('headCoach','')
            return item
        except Exception as ex:
            print(ex)


