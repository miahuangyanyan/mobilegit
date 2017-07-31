# -*- coding:utf-8 -*-

from scrapy.spider import CrawlSpider
import scrapy
import json
from JingdongSpider.items import JingdongspiderItem
import requests
import re
from scrapy.conf import settings
import pymongo
from time import sleep
import random


class JindongSpider(CrawlSpider):
    name = 'jingdong'
    start_urls = ['https://so.m.jd.com/ware/search.action']

    def __init__(self):
        CrawlSpider.__init__(self)
        connection = pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    brands = ['iPhone', '小米手机', '华为', '魅族手机', '三星手机', 'oppo手机', '乐视手机', '摩托罗拉手机', '360手机', '一加手机',
              '美图手机', '金立手机', '联想手机', '锤子手机', 'vivo手机']
    brand_page_num_dict = {'iPhone': 53, '小米手机': 75, '华为': 750, '魅族手机': 116, '三星手机': 79, 'oppo手机': 8, '乐视手机': 13,
                           '摩托罗拉手机': 52, '360手机': 22, '一加手机': 7, '美图手机': 18, '金立手机': 12, '联想手机': 20, '锤子手机': 8,
                           'vivo手机': 2}

    def parse_start_url(self, response):
        url = 'https://so.m.jd.com/ware/search.action'
        for brand, num in self.brand_page_num_dict.items():
            for i in range(1, num + 1):
                data = {'_format_': 'json', 'sort': '', 'page': str(i), 'keyword': brand}
                request = scrapy.FormRequest(url, formdata=data, callback=self.parse_brand_list)
                request.meta['brand'] = brand
                yield request

    def parse_brand_list(self, response):
        data = json.loads(response.text)
        search_data = json.loads(data['searchData'])
        ware_list = search_data['wareList']
        # print(type(ware_list))
        for ware in ware_list['wareList']:
            print(ware['wareId'] + ' ' + ware['wname'])
            item = JingdongspiderItem()
            phone_url = 'http://item.jd.com/' + ware['wareId'] + '.html'
            cursor = self.collection.find({'url': phone_url})
            if cursor.count() > 0:
                continue
            item['phone_name'] = ware['wname']
            item['url'] = phone_url
            item['brand'] = response.meta['brand']

            phone_reviews = []
            post_url = 'https://club.jd.com/comment/productPageComments.action'
            data_form = {
                'callback': 'fetchJSON_comment98vv61',
                'productId': str(ware['wareId']),
                'score': 0,
                'sortType': 5,
                'pageSize': 10,
                'isShadowSku': 0,
                'page': 0
            }
            s = requests.session()
            while True:
                t = s.get(post_url, params=data_form).text
                try:
                    t = re.search(r'(?<=fetchJSON_comment98vv61\().*(?=\);)', t).group(0)
                except Exception as e:
                    break
                j = json.loads(t)
                comment_list = j['comments']
                if len(comment_list) == 0:
                    break
                for comment in comment_list:
                    content = comment['content']
                    user_name = comment['nickname']
                    comment_time = comment['referenceTime']
                    score = comment['score']
                    comment = {'user_name': user_name, 'comment': content, 'comment_time': comment_time, 'score': score}
                    phone_reviews.append(comment)
                    print(comment)
                sleep(random.random())
                data_form['page'] += 1
            s.close()
            item['phone_reviews'] = phone_reviews
            item['source_platform'] = '京东'
            item['domain'] = 'www.jd.com'
            yield item
