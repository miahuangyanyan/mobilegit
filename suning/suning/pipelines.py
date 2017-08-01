# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo
class SuningPipeline(object):
        def __init__(self):
            # 连接数据库
            self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
            # 数据库登录账号密码
            # self.client.admin.authenticate(settings['MINGO_USER'],settings['MONGO_PSW'])
            # 数据库的句柄,collection 句柄
            self.db = self.client[settings['MONGO_DB']]
            self.coll = self.db[settings['MONGO_COLL']]

        # pipeline 默认调用
        def process_item(self, item, spider):
            postItem = dict(item)  # item 转为字典
            self.coll.insert(postItem)  # 数据库插入记录
            return item  # 控制台输出item 数据


