# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
class MongoDBPipeline(object):
    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection):
        connection = pymongo.MongoClient(mongodb_server, mongodb_port)
        self.mongodb_db = mongodb_db
        self.db = connection[mongodb_db]
        self.mongodb_collection = mongodb_collection
        self.collection = self.db[mongodb_collection]
    @classmethod
    def from_crawler(cls, crawler):
        # 连接mongodb
        return cls('192.168.200.47', 27017, 'spider', 'gome')
        #return cls('localhost', 27017, 'spider', 'gome')
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

# class GomePipeline(object):
#     def process_item(self, item, spider):
#         return item
