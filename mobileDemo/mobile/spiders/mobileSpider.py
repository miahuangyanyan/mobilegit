#_*_coding:utf-8 _*_
import sys,os
reload(sys)
import re

import  pymongo
from  bs4 import BeautifulSoup
sys.setdefaultencoding("utf-8")
from scrapy.spider import CrawlSpider
import requests
import scrapy

from mobile.items import  MobileItem
class mobileSpider(CrawlSpider):
    name = "mobileSpider"
    # 华为,三星，vivo,oppo,苹果，魅族，小米，美图,联想，华硕,酷派，索尼，锤子科技，HTC,惠普，黑莓，夏普，朵唯,乐视，TCL,荣耀
    start_urls = [
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_613_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_98_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1795_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1673_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_544_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1434_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_34645_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_35179_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1763_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_227_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1606_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_1069_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_35849_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_33080_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_223_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_12772_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_300_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_33855_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_33992_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_171_list_1.html",
                  "http://detail.zol.com.cn/cell_phone_index/subcate57_50840_list_1.html"
    
                   ]
    header = {
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
    }

    def parse_start_url (self, response):
        mobile_urls = response.xpath('//h3/a/@href').extract()  # 提取手机的url
        mobile_nexturls = response.xpath("//div[ @class='pagebar'][1]/a[2]/@href").extract_first() # 获取机型的下一页信息

        for url in  mobile_urls:


                yield  scrapy.Request(url= response.urljoin(url), callback=self.parse_page)
        if (mobile_nexturls):
            yield scrapy.Request(url=response.urljoin(mobile_nexturls), callback=self.parse_start_url)

    def parse_page(self,response):
         # 获取点评的链接
        comment_url = response.xpath(u"//div[ @id = 'tagNav']//a[text()='点评']/@href").extract_first()
        yield scrapy.Request(url=response.urljoin(comment_url), callback = self.parse_review_page)

    def  parse_review_page(self, response):
        #获取静态的第一页
          phone_review=[]
          for  info in response.xpath("//ul[@class='comment-list']//li"):

             item = MobileItem()
             phone_name = info.xpath("//div[@class ='breadcrumb']/a[4]/text()").extract_first()
             brand = info.xpath("//div[@class ='breadcrumb']/a[3]/text()").extract_first()
             url = info.xpath("//div[@class ='breadcrumb']/a[4]/@href").extract_first()
             url = response.urljoin(url)
             item['phone_name'] = phone_name
             item['brand'] = brand
             # item['brand'] = '华为荣耀'
             item['url'] = url
             user_name =  info.xpath("div[@class='comments-user']/div[@class='comments-user-name']/span/text()").extract_first()
             comment_time =  info.xpath("div[@class='comments-list-content']/div[@class='single-score clearfix']"
                                         "/span[@class='date']/text()").extract_first()
             select= info.xpath("div[@class='comments-list-content']/div[@class='comments-content']/"
                                "div[@class='J_CommentContent comment-height-limit']/div[@class='content-inner']")

             advantage = 0
             disadvantage = 0
             summary = 0
             comment={}

             #抓取优点，缺点，总结 数据
             if  (u'优点：'  == select.xpath("div[@class='comments-words']/strong[@class='good']/text()").extract_first()):
                 advantage += 1
             if (u'缺点：' == select.xpath("div[@class='comments-words']/strong[@class='bad']/text()").extract_first()):
                disadvantage += 1
             if (u'总结：' == select.xpath("div[@class='comments-words']/strong[@class='summary']/text()").extract_first()):
                summary += 1

             if (advantage ==1 and disadvantage ==1 and summary == 1):
                ad = select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
                dis = select.xpath("div[@class='comments-words'][2]/p/span/text()").extract_first()
                sum = select.xpath("div[@class='comments-words'][3]/p/span/text()").extract_first()
                comment = {'advantage': ad, 'disadvantage': dis, 'summary': sum}
             if (advantage == 1 and  disadvantage ==1 and summary ==0 ):
                ad= select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
                dis= select.xpath("div[@class='comments-words'][2]/p/span/text()").extract_first()
                comment = {'advantage': ad, 'disadvantage': dis}

             if (advantage == 1 and disadvantage == 0 and summary == 1):
                ad= select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
                sum = select.xpath("div[@class='comments-words'][2]/p/span/text()").extract_first()
                comment = {'advantage': ad, 'summary': sum}

             if (advantage == 1 and disadvantage == 0 and summary == 0):
               ad = select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
               comment = {'advantage': ad}

             if (advantage == 0 and disadvantage == 0 and summary == 1):
               sum = select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
               comment= {'summary': sum}

             if (advantage == 0 and disadvantage == 1 and summary == 0):
                dis = select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
                comment = { 'disadvantage': dis}

             if (advantage == 0 and disadvantage == 1 and summary == 1):
                dis = select.xpath("div[@class='comments-words'][1]/p/span/text()").extract_first()
                sum = select.xpath("div[@class='comments-words'][2]/p/span/text()").extract_first()
                comment= {'disadvantage': dis, 'summary': sum}
             phone_review.append({'user_name':user_name,'comment_time': comment_time,'comment':comment})
             # 动态获取下一页


          s = response.xpath(u"//div[@class='page']/a[text()='下一页']/@href").extract_first()
          if  s :
              product_id = re.compile(r'(proId)=(\d+)').search(s).group(2).encode('utf8')
              page = 2
              while True:
                  request_url = 'http://detail.zol.com.cn/xhr3_Review_GetListAndPage_isFilter=0%5EproId=' + product_id \
                                + '%5Epage=' + str(page) + '.html'

                  html = requests.get(request_url).json()['list']
                  soup = BeautifulSoup(html)
                  info_list = soup.find_all(name="li", attrs={"class": "comment-item"})
                  if len(info_list) == 0:
                      break
                  for info in info_list:   #  评论总数
                      advantage = 0
                      disadvantage = 0
                      summary = 0
                      comment = {}
                      comment_time = info.find(name="span", attrs={"class": "date"}).get_text()
                      user_name = info.find(name="div", attrs={"class": "comments-user-name"}).span.get_text()
                      comment_list = info.find_all(name='div', attrs={'class': 'comments-words'})

                      for content in comment_list:
                          if content.find_all(name='strong', attrs={'class': 'good'}):
                              advantage += 1
                          if content.find_all(name='strong', attrs={'class': 'bad'}):
                              disadvantage += 1
                          if content.find_all(name='strong', attrs={'class': 'summary'}):
                              summary += 1
                      if (advantage == 1 and disadvantage == 1 and summary == 1):
                          ad = comment_list[0].span.get_text().decode('utf8')
                          dis = comment_list[1].span.get_text().decode('utf8')
                          sum = comment_list[2].span.get_text().decode('utf8')

                          comment = {'advantage': ad, 'disadvantage': dis, 'summary': sum}
                      if (advantage == 1 and disadvantage == 1 and summary == 0):
                          ad = comment_list[0].span.get_text().decode('utf8')
                          dis = comment_list[1].span.get_text().decode('utf8')
                          comment = {'advantage': ad, 'disadvantage': dis}

                      if (advantage == 1 and disadvantage == 0 and summary == 1):
                          ad = comment_list[0].span.get_text().decode('utf8')
                          sum = comment_list[1].span.get_text().decode('utf8')
                          comment = {'advantage': ad, 'summary': sum}

                      if (advantage == 1 and disadvantage == 0 and summary == 0):
                          ad = comment_list[0].span.get_text().decode('utf8')
                          comment = {'advantage': ad}

                      if (advantage == 0 and disadvantage == 0 and summary == 1):
                          sum = comment_list[0].span.get_text().decode('utf8')
                          comment = {'summary': sum}

                      if (advantage == 0 and disadvantage == 1 and summary == 0):
                          dis = comment_list[0].span.get_text().decode('utf8')
                          comment = {'disadvantage': dis,}

                      if (advantage == 0 and disadvantage == 1 and summary == 1):
                          dis = comment_list[0].span.get_text().decode('utf8')
                          sum = comment_list[1].span.get_text().decode('utf8')
                          comment = {'disadvantage': dis, 'summary': sum}
                      phone_review.append({'user_name': user_name, 'comment_time': comment_time, 'comment': comment})

                  page += 1

              item ['source_platform'] = '中关村'
              item['domain'] = 'http://detail.zol.com.cn/'
              item['phone_reviews'] = phone_review
              yield item

























































