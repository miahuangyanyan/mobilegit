# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    phone_name = scrapy.Field()
    phone_reviews = scrapy.Field()
    domain = scrapy.Field()
    source_platform = scrapy.Field()
    record_date = scrapy.Field()
