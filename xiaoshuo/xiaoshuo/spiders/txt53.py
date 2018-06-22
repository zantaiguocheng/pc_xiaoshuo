# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spider import CrawlSpider, Rule

from xiaoshuo.items import XiaoshuoItem


class Txt53Spider(CrawlSpider):
    name = 'txt53'
    allowed_domains = ['www.txt53.com']
    start_urls = ['http://www.txt53.com']
    rules = [
        Rule(LinkExtractor(allow=('/txt\d+.html')),
             follow=False, callback='parse_itme'),
        Rule(LinkExtractor(
            allow=('/list_\d+_\d+.html')), follow=True),
        Rule(LinkExtractor(allow=('html/[a-z]+\w*/')), follow=False),
        # Rule(LinkExtractor(allow=('/down/\d+.html')), callback='parse_itme'),
    ]
    # def parse(self,response):
    #     links = LinkExtractor(allow=('html/xuanhuan/txt\d+.html'))
    #     link_list = links.extract_links(response)
    #     for link in link_list:
    #         yield Request(url=link.url, callback=self.zhongjian)

    # def zhongjian(self, response):
    # links = LinkExtractor(allow=('/down/\d+.html'))
    # link_list = links.extract_links(response)
    # for link in link_list:
    #     yield Request(url=link.url, callback=self.parse_itme)

    def parse_itme(self, response):
        print('1')
        x = Selector(response)
        names = x.xpath('//ul/li/b/text()').extract()
        leibie = x.re('小说分类：([\u4e00-\u9fa5]+)')
        links = LinkExtractor(allow=('/down/\d+.html'))
        link_list = links.extract_links(response)
        for link in link_list:
            yield Request(url=link.url, callback=self.parse_itme1, meta={'name': names, 'leibie': leibie})

    def parse_itme1(self, response):
        itme = XiaoshuoItem()
        url = response.xpath('//ul/li/a[@rel="nofollow"]/@href').extract()[1]
        itme['file_urls'] = [url]
        itme['names'] = response.meta['name']
        itme['leibie'] = response.meta['leibie']
        yield itme
