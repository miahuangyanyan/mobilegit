# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class MobileItem(scrapy.Item):
    # define the fields for your item here like:
    phone_name = Field()
    source_platform = Field()
    domain = Field()
    url = Field()
    brand = Field()
    phone_reviews= Field()
    pass
