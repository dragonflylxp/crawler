# -*- coding: utf-8 -*-

# Scrapy settings for amazon_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'amazon_scrapy'

SPIDER_MODULES = ['amazon_scrapy.spiders']
NEWSPIDER_MODULE = 'amazon_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazon_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 不遵守Robot协议文件
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
# 并发数量(默认是16个)
CONCURRENT_REQUESTS = 8 
# 设置下载延时,默认为0
DOWNLOAD_DELAY = 0
# 在每个域下允许发起请求的最大并发数(默认是8个)
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# 针对每个ip允许发起请求的最大并发数量(默认0个)
CONCURRENT_REQUESTS_PER_IP = 1
# 不允许cookies
COOKIES_ENABLED = False

# 启用重试
RETRY_ENABLED = True
#包括第一次下载，最多的重试次数
RETRY_TIMES=3

# 超时时间
DOWNLOAD_TIMEOUT = 120
# 关闭重定向
REDIRECT_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazon_scrapy.middlewares.AmazonScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'amazon_scrapy.middlewares.AmazonScrapyDownloaderMiddleware': 543,
#}
# 其后数字越小表示优先级越高，越先执行
DOWNLOADER_MIDDLEWARES = {
   'amazon_scrapy.middlewares.RotateUserAgentMiddleware': 543,
   'amazon_scrapy.middlewares.ProxyMiddleware': 544,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
   #'scrapy.downloadermiddlewares.retry.RetryMiddleware':600,
}



# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'amazon_scrapy.pipelines.AmazonScrapyPipeline': 300,
#}

ITEM_PIPELINES = {
   #'amazon_scrapy.pipelines.CSVPipeline': 200,
   'amazon_scrapy.pipelines.RabbitMQPipeline': 300,
   #'amazon_scrapy.schedulers.ZhimaProxyScheduler': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# 动态下载延时
AUTOTHROTTLE_ENABLED = True

AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0



# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 日志级别
LOG_LEVEL = 'DEBUG'
#LOG_FILE = 'access.log'

# redis队列的信息
REDIE_URL = None
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
FILTER_DB = 0
REDIS_PROXIES_KEY="proxy.ip.pool"
REDIS_PARAMS = {
   'password': '',
}

# Rabbit 配置

RABBIT_MQ_HOST = '127.0.0.1'
RABBIT_MQ_PORT = '5672'
RABBIT_MQ_VIRTUAL_HOST= '/'
RABBIT_MQ_USER = 'rabbit'
RABBIT_MQ_PASSWORD ='123456'
RABBIT_MQ_QUEUE = "Spider_Output_Queue1"
RABBIT_MQ_ROUTING_KEY="Spider_Output_Queue1"

# 代理配置
PROXY_URL ="http://tiqu.linksocket.com:81/abroad?num=1&type=1&pro=0&city=0&yys=0&port=1&flow=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=0&regions="
PROXY_CRON ="*/59"

# # 代理IP池
# PROXIES = [
#    '58.218.214.146:9909'
# ]
PROXY_LUMINATI = "127.0.0.1:24000"
