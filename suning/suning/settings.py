# -*- coding: utf-8 -*-

# Scrapy settings for suning project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'suning'

SPIDER_MODULES = ['suning.spiders']
NEWSPIDER_MODULE = 'suning.spiders'

# #启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# #确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'suning (+http://www.yourdomain.com)'


# Scrapy settings for mobile project

ITEM_PIPELINES={
    'suning.pipelines.SuningPipeline':300,
    # 'scrapy_redis.pipelines.RedisPipeline': 301
}

#mongodb 数据库的配置信息
#
# MONGO_HOST = '127.0.0.1' #主机ip
MONGO_PORT = 27017
#MONGO_DB = 'spider'#库名
MONGO_DB = 'mobile_spider'#库名
MONGO_COLL = 'suning' #collection 名
MONGO_HOST = '192.168.200.47' #主机ip

#伪装浏览器请求，设置延迟抓取，防ban
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
ROBOTSTXT_OBEY=False
DOWNLOAD_DELAY = 0.25 # 250 ms of delay
LOG_LEVEL = 'INFO'
# REDIS_URL = 'redis://root:@127.0.0.1:6379'
# REDIS_URL ='redis://root:redistest@192.168.200.47:6379'

DOWNLOADER_MIDDLEWARES = {
    'suning.middlewares.MyCustomDownloaderMiddleware': None,
    'suning.middlewares.SuningSpiderMiddleware':500
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'suning.middlewares.SuningSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'suning.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'suning.pipelines.SuningPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
