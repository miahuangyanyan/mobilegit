from scrapy.spiders import CrawlSpider
import scrapy
import json
from JingdongSpider.items import JingdongspiderItem
import requests
import re
from scrapy.conf import settings
import pymongo
from time import sleep
import random
import datetime


class JDSpider(CrawlSpider):
    name = 'jd'
    start_urls = ['https://wwww.jd.com/']

    def __init__(self):
        CrawlSpider.__init__(self)
        connection = pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    brands = ['iPhone', '小米手机', '华为手机', '魅族手机', '三星手机', 'oppo手机', '乐视手机', '摩托罗拉手机', '360手机', '一加手机',
              '美图手机', '金立手机', '联想手机', '锤子手机', 'vivo手机']

    # brands = ['iPhone']

    def parse_start_url(self, response):
        for brand in self.brands:
            for i in range(1, 50):
                url = "https://search.jd.com/Search?keyword=" + brand + "&enc=utf-8&page=" + str(i * 2 - 1)
                yield scrapy.Request(url=url, callback=self.parse_product_url, meta={'brand': brand})

    def parse_product_url(self, response):
        # urls = response.xpath('//div[@class ="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        # for i in urls:
        #     url = response.urljoin(i)
        #     yield Request(url=url, callback=self.product)
        for li in response.xpath('//li[@class="gl-item"]'):
            product_id = li.xpath('@data-sku').extract_first()
            product_url = li.xpath(
                'div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract_first()
            request = scrapy.Request(url=response.urljoin(product_url), callback=self.parse_product)
            request.meta['product_id'] = product_id
            request.meta['brand'] = response.meta['brand']
            yield request

    def parse_product(self, response):
        product_name = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li[1]/@title').extract_first()
        product_id = response.meta['product_id']
        print(product_name + ' ' + product_id)

        item = JingdongspiderItem()
        phone_url = 'http://item.jd.com/' + product_id + '.html'
        cursor = self.collection.find({'url': phone_url})
        if cursor.count() > 0:
            return
        item['phone_name'] = product_name
        item['url'] = phone_url
        item['brand'] = response.meta['brand']


        phone_reviews = []
        post_url = 'https://club.jd.com/comment/productPageComments.action'
        data_form = {
            'callback': 'fetchJSON_comment98vv61',
            'productId': str(product_id),
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
        item['record_date'] = str(datetime.date.today())
        yield item
