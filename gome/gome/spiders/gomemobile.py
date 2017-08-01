# coding:utf-8
from scrapy.spider import CrawlSpider
import time
import random
import json
import requests
import scrapy
import urlparse
from gome.items import GomeItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class DmozSpider(CrawlSpider):
    name = 'gome'
    download_delay = 3
  #  allowed_domains = ["amazon.cn"]
    #苹果,联想,华为，OPPO，vivo，魅族，三星，HTC
    start_urls = [
        'http://search.gome.com.cn/search?question=Apple&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=%E5%8D%8E%E4%B8%BA&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=lenovo&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=%E8%8D%A3%E8%80%80&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=OPPO&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=vivo&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=%E9%AD%85%E6%97%8F&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=%E4%B8%89%E6%98%9F&catId=cat10000070&page=1',
        'http://search.gome.com.cn/search?question=htc&catId=cat10000070&page=1',
        ]

    def start_requests(self):

        len_url = len(self.start_urls)
        for i in xrange(len_url):
            # brand=self.brands[i]
            url=self.start_urls[i]

            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        print "-------------list-----------"
        url_start=response.url
        print url_start
        # url_list=response.xpath('//*[@id="product-box"]//div/div/p[1]/a')
        url_list = response.xpath('//*[@id="product-box"]/li/div/p[2]/a/@href').extract()
        print len(url_list)
        if url_list:
            for url in url_list:
                print url
                yield scrapy.Request(url, callback=self.parse_mobile)
            pageNum = 0
            page = ''
            aa = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(url_start).query).items()])
            if aa.has_key('page'):
                page = aa['page']
                pageNum = int(page)
            url_len = len(url_start)
            page_len = len(page)
            pageNum += 1
            url = url_start[0:url_len - page_len] + str(pageNum)
            yield scrapy.Request(url,callback=self.parse)
    def parse_mobile(self,response):
        print "---------------mobile------------------------"
        item=GomeItem()
        url=response.url
        #brand；model；phone_name
        brand=response.xpath('//*[@id="prd_data"]/li[2]/ul[1]/li[4]/span[2]/text()').extract_first()
        model=response.xpath('//*[@id="prd_data"]/li[2]/ul[1]/li[5]/span[2]/text()').extract_first()
        phone_name = brand + ' ' + model
        brand=brand.encode("GBK", "ignore")
        if brand=='荣耀':
            brand='华为'
        #_id和url
        end=url.find('-')
        _id=url[24:end]
        print url
        print brand.encode("GBK", "ignore")
        print model.encode("GBK", "ignore")
        print phone_name.encode("GBK", "ignore")
        print _id
        phone_reviews = []
        for i in xrange(29):
            i=i+1
            good_url="http://ss.gome.com.cn/item/v1/prdevajsonp/appraiseNew/"+_id+"/%d/good/0/flag/appraise"%i
            #解析json
            con = requests.get(good_url)
            con = con.text
            conjson = json.loads(con, "gbk")
            json_comment = conjson['evaList']['Evalist']
            if json_comment:
                print "++++++++++++++++good++++++++++++++"
                for j in xrange(len(json_comment)):
                    content=json_comment[j]['appraiseElSum']
                    nikename=json_comment[j]['loginname']
                    comment_time=json_comment[j]['post_time']
                    score=json_comment[j]['mscore']
                    #style = json_comment[j]['skuInfo']
                    comment={'comment':content,'user_name':nikename,'comment_time':comment_time,'score':score}
                    phone_reviews.append(comment)
        mid_page=1
        while 1:
            mid_url="http://ss.gome.com.cn/item/v1/prdevajsonp/appraiseNew/"+_id+"/%d/mid/0/flag/appraise"%mid_page
            # 解析json
            con = requests.get(mid_url)
            con = con.text
            conjson = json.loads(con, "gbk")
            json_comment = conjson['evaList']['Evalist']
            if json_comment:
                mid_page+=1
                for j in xrange(len(json_comment)):
                    print "++++++++++++++++++++mid++++++++++++"
                    content = json_comment[j]['appraiseElSum']
                    nikename = json_comment[j]['loginname']
                    comment_time = json_comment[j]['post_time']
                    score = json_comment[j]['mscore']
                    #style=json_comment[j]['skuInfo']
                    comment = {'comment': content, 'user_name': nikename, 'comment_time': comment_time, 'score': score}
                    phone_reviews.append(comment)
            else:
                break
            if mid_page>30:
                break
        bad_page = 1
        while 1:
            bad_url = "http://ss.gome.com.cn/item/v1/prdevajsonp/appraiseNew/" + _id + "/%d/bad/0/flag/appraise" % bad_page
            # 解析json
            con = requests.get(bad_url)
            con = con.text
            conjson = json.loads(con, "gbk")
            json_comment = conjson['evaList']['Evalist']
            if json_comment:
                bad_page+=1
                for j in xrange(len(json_comment)):
                    print "++++++++++++++++mid++++++++++++++"
                    content = json_comment[j]['appraiseElSum']
                    nikename = json_comment[j]['loginname']
                    comment_time = json_comment[j]['post_time']
                    score = json_comment[j]['mscore']
                    #style = json_comment[j]['skuInfo']
                    comment = {'comment': content, 'user_name': nikename, 'comment_time': comment_time, 'score': score}
                    phone_reviews.append(comment)
            else:
                break
            if bad_page>30:
                break
        if phone_reviews:
            item['_id'] = _id
            item['url'] = url
            item['brand'] = brand
            item['model'] = model
            item['phone_name'] = phone_name
            item['phone_reviews'] = phone_reviews
            item['platform'] = '国美'
            yield item
        time.sleep(3 + random.random())
