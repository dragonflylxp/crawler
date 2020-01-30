'''
@Author: kaybinwong
@Since: 1.0.0
@Date: 2020-01-10
'''
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random

import redis
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
    随机设置User-Agent,防止反爬
    """

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        # 随机生成agent
        agent = UserAgent(use_cache_server=False).chrome
        if agent:
            # logging.info(ua)
            logging.info("随机生成的User-Agent %s" % agent)
            request.headers['User-Agent'] = agent

class ProxyMiddleware(object):

    #def __init__(self, host,port,password,key):
        #self.redisClient = redis.Redis(host=host,port=port,password=password)
        #self.key = key
    def __init__(self, proxy=None):
        self.proxy = proxy

    @classmethod
    def from_crawler(cls, crawler):
        #host = crawler.settings.get('REDIS_HOST')
        #port = crawler.settings.get('REDIS_PORT')
        #password = crawler.settings.get('REDIS_PASSWORD')
        #key = crawler.settings.get('REDIS_PROXIES_KEY')
        #return cls(host,port,password,key)
        proxy_luminati = crawler.settings.get('PROXY_LUMINATI')
        return cls(proxy_luminati)

    def process_request(self, request, spider):
        #ip = self._get_random_proxy()
        logging.info("获取到的代理ip:%s" % self.proxy)
        if self.proxy is not None:
            request.meta['proxy'] = self.proxy 

    def _get_random_proxy(self):
        """
        随机获取ip
        """
        # response = requests.get('http://http.tiqu.alicdns.com/getip3?num=199&type=1&pro=&city=0&yys=0&port=11&pack=80344&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4')
        # ip_pools = response.text
        #
        # proxy = random.choice(ip_pools.split("\n")).strip()
        #ip_pools =\
            # "122.188.243.238:4254,123.179.129.247:4260,124.112.236.99:4204,110.90.175.17:4263,60.188.58.28:4274,112.192.255.109:4284,114.237.55.83:4214,114.104.130.38:4227,218.91.122.101:4282,117.63.136.43:4276,182.34.17.82:4234,183.161.227.144:4241,180.122.253.139:4296,183.166.161.128:4270,58.243.205.119:4243,182.108.46.95:4248,180.118.100.74:4207,114.238.59.166:4221,27.209.15.167:4246,36.33.20.49:4226,114.103.137.235:4276,60.177.90.41:4217,36.6.154.116:4290,49.79.67.112:4256,60.188.59.161:4274,117.94.213.118:4216,119.5.189.80:4258,183.161.0.243:4260,175.155.51.198:4258,180.124.130.102:4258,125.111.146.173:4205,49.79.65.79:4256,175.42.169.112:4293,220.189.97.34:4236,223.242.246.124:4231,218.91.64.183:4282,124.113.217.148:4251,119.185.235.84:4251,114.100.0.16:4231,114.104.131.99:4226,117.63.133.229:4276,112.84.215.14:4207,218.95.113.155:4213,218.91.104.183:4282,49.79.66.78:4218,106.35.33.129:4254,36.34.14.212:4226,180.123.84.144:4243,182.108.168.133:4262,175.153.245.60:4284,14.134.109.86:4272,114.101.253.206:4204,180.109.33.59:4266,121.206.28.21:4254,121.56.215.107:4281,106.56.221.55:4228,114.104.130.33:4226,218.91.132.59:4226,123.169.37.223:4234,125.111.147.130:4205,61.166.41.5:4228,119.132.24.45:4272,60.187.226.113:4275,49.70.183.196:4207,111.126.94.58:4283,49.71.34.46:4282,111.72.150.250:4221,114.103.91.135:4242,182.247.61.141:4273,123.156.177.255:4281,220.185.1.132:4276,183.161.227.70:4251,182.99.226.58:4245,110.52.224.126:4246,223.243.208.243:4254,223.241.28.182:4287,36.248.140.22:4261,112.113.154.92:4256,60.185.40.48:4276,112.114.156.127:4228,117.94.158.209:4253,114.102.42.223:4216,221.231.88.74:4232,117.66.84.133:4231,115.151.206.7:4236,122.242.63.242:4256,183.165.11.213:4235,117.57.36.14:4273,117.57.37.178:4273,58.63.37.60:4206,175.44.109.142:4254,117.44.69.41:4236,117.68.244.116:4251,163.179.206.18:4225,220.178.146.63:4254,106.122.169.60:4202,182.108.168.179:4262,36.57.91.177:4226,112.84.244.195:4207,182.99.224.132:4217,182.99.224.187:4245,114.237.62.241:4214,182.99.225.81:4245,125.118.78.216:4204,117.67.126.229:4227,183.161.229.8:4241,175.42.158.127:4254,182.110.21.55:4248,113.100.89.48:4236,106.122.168.247:4202,111.72.150.13:4231,182.244.123.83:4228,117.69.129.183:4248,111.75.117.36:4262,220.179.219.48:4276,223.214.207.187:4204,182.247.60.24:4273,117.94.117.181:4216,114.99.6.125:4276,36.34.14.170:4226,115.209.122.119:4226,125.111.147.196:4205,183.166.119.81:4231,182.108.62.195:4248,112.111.77.116:4254,222.90.46.220:4268,114.238.91.246:4221,117.94.158.191:4236,117.90.216.79:4216,112.85.125.147:4250,182.99.226.144:4227,222.220.152.167:4267,123.179.129.211:4260,125.111.146.248:4205,125.111.150.76:4205,111.75.117.144:4262,60.169.222.128:4241,111.72.108.164:4213,123.179.130.91:4260,111.72.151.151:4231,117.28.97.119:4202,125.111.147.106:4205,119.185.235.110:4251,182.108.168.234:4262,1.182.193.88:4261"
        # proxy = random.choice(ip_pools.split(","))
        # return proxy
        try:
            porxys = str(self.redisClient.get(self.key),'utf-8')

            return  random.choice(porxys.split(","))
        except Exception as ex:
            logging.error("获取代理ip失败%s" % ex)
            return  None



# class ProxyMiddleware(object):
#     # overwrite process request
#     def process_request(self, request, spider):
#         # Set the location of the proxy
#         sql = 'select ip,port from t_proxy_ip t where t.is_valid =1'
#         result = SqlUtil.query_all(sql)
#         ip_port = random.choice(result)
#         logging.info(ip_port)
#         request.meta['proxy'] = "http://{0}:{1}".format(ip_port['ip'], ip_port['port'])
#         # # Use the following lines if your proxy requires authentication
#         # proxy_user_pass = "USERNAME:PASSWORD"
#         # # setup basic authentication for the proxy
#         # encoded_user_pass = base64.encodestring(proxy_user_pass)
#         # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
