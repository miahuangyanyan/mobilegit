# -*-coding: utf-8 -*-

import re
import scrapy
import json
import requests
from scrapy.spider import Spider
from suning.items import SuningItem
import urllib
from bs4 import BeautifulSoup
class suningSpider(Spider):
    name = "suningSpider"
    #苹果，荣耀,华为，三星，oppo,vivo,HTC
    start_urls = ["https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-10103.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-964259.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-10011.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-12256.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-19311.html",
                  "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-10032.html",
                  ]

    def parse(self, response):
        pro= str(response)
        p = re.compile('-0-0-0-')
        tail = p.split(pro)[2]

        mobile_urls = response.xpath("//div[@class='res-info']/p[@class='sell-point']/a[@class='sellPoint']/@href").extract()
        for mobile_url in mobile_urls:
            yield scrapy.Request(url=response.urljoin(mobile_url), callback=self.parse_page)
        total_page= response.xpath("//div[@class='little-page']/span").extract_first()

        s = str(total_page)
        p = re.compile('>/')
        mid = p.split(s)[1]
        p2 = re.compile('</')
        pages= p2.split(mid)[0]
        print "----------total pages------"
        print  pages

        head = "https://list.suning.com/0-20006-"
        mid = "-0-0-0-0-0-0-0-"

        for  i in range(1,int(pages),1):
            next_page = head+ str(i)+ mid+tail
            print next_page
            yield scrapy.Request(url=next_page, callback=self.parse)


        # while  True:
        #
        #     page = 1
        #     head = "https://list.suning.com/emall/showProductList.do?ci=20006&pg=03&cp=" + str(
        #         page) + "&il=0&iy=-1&hf=brand_Name_FacetAll:"
        #     name = response.xpath("//*[@id='search-path']/dl[2]/dt/em").extract_first()
        #
        #     testname= response.xpath("//dl[@class='goods-special down top']/dt/em").extract_first()
        #
        #     print "--------------name======="
        #     print testname
        #     english, chinese = self.match(testname)
        #     if (len(chinese) == 0):
        #         tail = "&adNumber=0&n=1&sesab=A&id=IDENTIFYING&cc=022"
        #         next_url = head + str(english) + tail
        #         print "---------obly english"
        #
        #     else:
        #         tail = "%29&adNumber=0&n=1&sesab=A&id=IDENTIFYING&cc=022"
        #         next_url = head + str(chinese) + str('%28') + str(english) + tail
        #         print '-----chinese and english'
        #     page += 1
        #     print "--------------request  next page"
        #     print next_url
        #     # html = requests.get(next_url)
        #     # url=html.xpath("//p[@class='sell-point']/a[1]/@href").extract()


    def match(self,name):
        print name
        reEnglish= re.compile("([a-zA-Z].*[a-zA-Z])")
        english = reEnglish.findall(name)
        reChinese = re.compile('[\x80-\xff]+')
        chinese = reChinese.findall(name)
        chinese = urllib.quote(" ".join(chinese))
        print "-------------match"
        print english[0]
        print chinese
        return english[0],chinese

    def deal_re(self,response):
        s = str(response)
        #<200 https://product.suning.com/0070060611/614080514.html>
        p = re.compile('/')
        num2 = p.split(s)[3]
        p2 =  re.compile('\.')
        num1 = p2.split(p.split(s)[4])[0]
        return num1, num2

    def parse_page(self, response):

        num1,num2= self.deal_re(response)
        page=1
        phone_reviews=[]
        item = SuningItem()
        item['url'] = response.xpath('//*[@id="productName"]/a/@href').extract_first()
        item['brand'] = response.xpath("//div[@class='dropdown'][3]/span/a/text()").extract_first()


        print "---item url"
        print item['url']
        print item['brand']
        #brand 这里有问题
        while True:
            request_url =  'https://review.suning.com/ajax/review_lists/general-000000000'+ str(num1) +'-'+ str(num2) +\
                          '-total-'+str(page) +'-default-10-----reviewList.htm?callback=reviewList'
            print "------------request"
            print request_url
            response_url = requests.get(request_url).text
            con = response_url.replace('reviewList(', '')
            conjson = con[0:-1]
            comment_list= json.loads(conjson,'gbk')['commodityReviews']
            if (len(comment_list) == 0):
                break
            for comment in comment_list:
                content = comment['content']
                user_name = comment['userInfo']['nickName']
                comment_time = comment['publishTime']
                phone_name = comment['commodityInfo']['commodityName']
                comment ={'user_name': user_name,'comment_time':comment_time,'content':content}
                item['phone_name'] = phone_name
                print content
                print user_name
                print comment_time
                print phone_name

                phone_reviews.append(comment)
                print "-------------check2"
            print len(phone_reviews)
            page += 1
        review_length = len(phone_reviews)
        item['phone_reviews'] = phone_reviews
        print "successful crawl"  +str(review_length)
        item['source_platform'] ='苏宁易购'
        item['domain'] = 'https://list.suning.com/'

        yield item






























