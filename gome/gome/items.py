# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()  # 手机url
    phone_name = scrapy.Field()  # 机型
    model = scrapy.Field()
    brand = scrapy.Field()  # 品牌
    average_score = scrapy.Field()  # 平均评分
    platform = scrapy.Field()  # 来源
    phone_reviews = scrapy.Field()  # 评论相关
    pass
