# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaoshuoPipeline(object):
    def process_item(self, item, spider):
        return item


from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline


class XiazaiPipeline(FilesPipeline):
    def get_media_requests(self, itme, info):
        return Request(url=itme['file_urls'][0], meta={'leibie': itme['leibie'][0], 'name': itme['names'][0]})

    def file_path(self, request, response=None, info=None):
        return '%s/%s.txt' % (request.meta['leibie'], request.meta['name'])
