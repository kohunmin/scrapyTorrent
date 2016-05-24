# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class TobestItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    hit = scrapy.Field()
    createTime = scrapy.Field()
    nowDateTime = scrapy.Field()
    diffSeconds = scrapy.Field()
    downUrlFile = scrapy.Field()
    file_paths = scrapy.Field()

