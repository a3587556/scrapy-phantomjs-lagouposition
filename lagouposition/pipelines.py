# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LagoupositionPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('localhost', 27017)
        db=connection['lagou']
        self.collection=db['positions']
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            log.msg("add data to MongoDB!", level=log.DEBUG, spider=spider)
        return item
