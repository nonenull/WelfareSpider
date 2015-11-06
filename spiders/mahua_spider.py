# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from spider.items import BedItem
from scrapy.spiders import Rule

#快乐麻花__爬虫
class MaHuaSpider(CrawlSpider):
    name = "mahua"
    allowed_domains = ["www.mahua.com"]
    start_urls = [
        "http://www.mahua.com/newjokes"
    ]
    rules = [
        # 定义爬取URL的规则
        # Rule(LinkExtractor(allow=("/pic/")), follow=True, callback='parse_item_picture')#picture分类
        # Rule(LinkExtractor(allow=("/text/")), follow=True, callback='parse_item_text')#text分类
        Rule(LinkExtractor(allow=("/gif/")), follow=True, callback='parse_item_gif')#gif分类
    ]

    def parse_item_picture(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.mahua')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.joke-title a::text').extract()
            item['content'] = detail.css('.content img::attr(src)').extract()
            item['preview'] = ''
            item['description'] = ''
            item['classify'] = 'picture'
            item['refer'] = self.name
            if item['title'] and item['content']:
                items.append(item)
        return items

    def parse_item_text(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.mahua')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.joke-title a::text').extract()
            item['content'] = detail.css('.content::text').extract()
            item['preview'] = ''
            item['description'] = ''
            item['classify'] = 'text'
            item['refer'] = self.name
            if item['title'] and item['content']:
                items.append(item)

        return items

    def parse_item_gif(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.mahua')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.joke-title a::text').extract()
            item['content'] = detail.css('.content img::attr(src)').extract()
            item['preview'] = ''
            item['description'] = ''
            item['classify'] = 'gif'
            item['refer'] = self.name
            if item['title'] and item['content']:
                items.append(item)
        return items

    def _process_request(self, request):
        print('process: ' + str(request))
        return request