# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class PrintPipeline(object):

    def process_item(self, item, spider):
        print "aaaaaaaaaaaaa=========="
        print item['title']
        return item

class dateOverPipeLines(object):
    def process_item(self, item, spider):
        if item['diffSeconds'] < 10000 :
            return item
        else :
            raise DropItem("dateOver %s" % item['downUrlFile'])


class TorrentPipelines(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return request.meta['file_paths']

    def get_media_requests(self, item, info):
        file_url = item['downUrlFile']
        yield scrapy.Request(file_url, meta=item, headers={'Referer':item['url']})

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no images")
        item['file_paths'] = file_paths
        return item
