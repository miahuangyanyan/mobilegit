# coding:utf-8
from scrapy.spider import CrawlSpider
import time
import random
import scrapy
import urlparse
from amazon.items import AmazonItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DmozSpider(CrawlSpider):
    name = 'amazon'
    download_delay = 3
  #  allowed_domains = ["amazon.cn"]
    #苹果,联想,华为，OPPO，vivo，魅族，小米，三星，索尼，HTC
    start_urls = [
        'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A664978051%2Cn%3A665002051%2Ck%3AApple&page=1&keywords=Apple&ie=UTF8&qid=1500625982',
        'https://www.amazon.cn/s/ref=nb_sb_noss_2?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=node%3D665002051&keywords=%E8%81%94%E6%83%B3',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3A%E5%8D%8E%E4%B8%BA&keywords=%E5%8D%8E%E4%B8%BA&ie=UTF8&qid=1500989757',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3AOPPO&keywords=OPPO&ie=UTF8&qid=1500989679',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3Avivo&keywords=vivo&ie=UTF8&qid=1500989619',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3A%E9%AD%85%E6%97%8F&keywords=%E9%AD%85%E6%97%8F&ie=UTF8&qid=1500989364',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3A%E5%B0%8F%E7%B1%B3&keywords=%E5%B0%8F%E7%B1%B3&ie=UTF8&qid=1500989289',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3A%E4%B8%89%E6%98%9F&keywords=%E4%B8%89%E6%98%9F&ie=UTF8&qid=1500988418',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3A%E7%B4%A2%E5%B0%BC&keywords=%E7%B4%A2%E5%B0%BC&ie=UTF8&qid=1500988525',
        'https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A664978051%2Cn%3A665002051%2Ck%3AHTC&keywords=HTC&ie=UTF8',
        ]

    def start_requests(self):

        len_url = len(self.start_urls)
        for i in xrange(len_url):
            # brand=self.brands[i]
            url=self.start_urls[i]

            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        url=response.url
        aa = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(url).query).items()])
        brand = []
        if aa.has_key('keywords'):
            brand = aa['keywords']
        time.sleep(3 + random.random())
        mobile_urls = response.xpath('//*[@id="s-results-list-atf"]//div/div[3]/div[1]/a/@href').extract()  # 手机url
        mobile_nexturls = response.xpath('//*[@id="pagnNextLink"]/@href').extract_first()
        for url in mobile_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url,meta={'brand':brand}, callback=self.parse_mobile)
        if mobile_nexturls:
            yield scrapy.Request(url=response.urljoin(mobile_nexturls), callback=self.parse)
    def parse_mobile(self,response):
        #url和brand
        item = AmazonItem()
        url=response.url
        print "-----------------amazon--------------"
        print url
        brand=response.meta['brand']
        item['brand']=brand
        item['url']=url
        #_id
        aa = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(url).query).items()])
        qid = []
        if aa.has_key('qid'):
            qid = aa['qid']
        count=response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        if count:
            count = count.encode("GBK", "ignore")
            end = count.find(' ')
            id = qid + count[0:end]
        else:
            id=qid+'0'
        item['_id']=id
        #型号
        attribute_list=response.xpath('//*[@id="prodDetails"]//div[1]/div/div[2]/div/div/table/tbody/tr/td[1]/text()').extract()
        value_list=response.xpath('//*[@id="prodDetails"]//div[1]/div/div[2]/div/div/table/tbody/tr/td[2]/text()').extract()
        len_list=len(attribute_list)
        temp='型号'
        temp=temp.encode("GBK", "ignore")
        item['model']=''
        for i in xrange(len_list):
            attribute = attribute_list[i].encode("GBK", "ignore")
            if attribute == temp:
                model = value_list[i]
                item['model'] = model
        #phone_name
        phone_name=brand+' '+item['model']
        item['phone_name']=phone_name
        #平均分
        average_score = response.xpath('//*[@id="summaryStars"]/a/i/span/text()').extract_first()
        item['average_score'] = average_score
        #进入评论页
        review_list = []
        review_url=response.xpath('//*[@id="revF"]/div/a/@href').extract_first()
        if review_url:
            url = review_url + "&pageNumber=1"
            yield scrapy.Request(url,meta={'review_list':review_list,'item':item},callback=self.parse_review)
            #yield scrapy.Request(review_url,callback=self.parse_review)



    def parse_review(self,response):
        print "---------------review-----------"
        print response.url
        item = response.meta['item']
        review_list=response.meta['review_list']
        comments_detail =response.xpath('//*[@id="cm_cr-review_list"]/div')
        for comment_detail in comments_detail:
            content=comment_detail.xpath('div/div[4]/span/text()').extract_first()
            nikename=comment_detail.xpath('div/div[2]/span[1]/a/text()').extract_first()
            date = comment_detail.xpath('div/div[2]/span[4]/text()').extract_first()
            score = comment_detail.xpath('div/div[1]/a/@title').extract_first()
            if score:
             score = score[0:3]
            detail_list=comment_detail.xpath('div/div[3]/a/text()').extract()
            color=''
            memory=''
            num=len(detail_list)
            print num
            if num==2:
                if detail_list[0].find('：') >= 0:
                    start = detail_list[0].find('：')
                    end = len(detail_list[0])
                    memory = detail_list[0][start + 1:end]
                    print memory.encode("GBK", "ignore")
                elif detail_list[0].find(':') >= 0:
                    start = detail_list[0].find(':')
                    end = len(detail_list[0])
                    memory = detail_list[0][start + 1:end]
                    print memory.encode("GBK", "ignore")
                if detail_list[1].find('：') >= 0:
                    start = detail_list[1].find('：')
                    end = len(detail_list[1])
                    color = detail_list[1][start + 1:end]
                elif detail_list[1].find(':') >= 0:
                    start = detail_list[1].find(':')
                    end = len(detail_list[1])
                    color = detail_list[1][start + 1:end]
            style=memory+' '+color
            comment = {'comment': content, 'user_name': nikename, 'comment_time': date, 'style':style,'score':score}
            review_list.append(comment)
        next_url = response.xpath("//li[@class='a-last']/a/@href").extract_first()
        if next_url:
            review_url=response.url
            pageNum=0
            page=''
            aa = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(review_url).query).items()])
            if aa.has_key('pageNumber'):
                page = aa['pageNumber']
                pageNum=int(page)
            url_len=len(review_url)
            page_len=len(page)
            pageNum+=1
            url=review_url[0:url_len-page_len]+str(pageNum)
            print "+++++++++++++++++++++++++++"
            print url
            yield scrapy.Request(url, meta={'review_list': review_list, 'item': item}, callback=self.parse_review)
        else:
            item['platform'] = '亚马逊'
            item['phone_reviews'] = review_list
            # print item['url']
            # print item['brand'].encode("GBK", "ignore")
            # print item['model'].encode("GBK", "ignore")
            # print item['phone_name'].encode("GBK", "ignore")
            # print item['average_score'].encode("GBK", "ignore")
            # print item['platform'].encode("GBK", "ignore")
            # print item['phone_reviews']
            yield item


