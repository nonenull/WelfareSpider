# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from spider.items import BedItem
from scrapy.spiders import Rule

#百思不得姐__爬虫
class BudejieSpider(CrawlSpider):
    name = "budejie"
    allowed_domains = ["www.budejie.com"]
    start_urls = [
        "http://www.budejie.com"
    ]
    rules = [
        # 定义爬取URL的规则
        # Rule(LinkExtractor(allow=("/pic/")), follow=True, callback='parse_item_picture'),#图片分类
        Rule(LinkExtractor(allow=("/text/")), follow=True, callback='parse_item_text')#段子分类
    ]

    # 处理段子分类，提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item_text(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.j-r-list')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.j-r-list-tool-ct-fx ::attr(data-text)').extract()
            item['content'] = detail.css('.j-r-list-c-desc ::text').extract()
            item['classify'] = 'text'
            item['preview'] = ''
            item['description'] = ''
            if item['title'] and item['content'] :
                items.append(item)
        return items

    # 处理图片分类，提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item_picture(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.j-r-list')
        for detail in detail_div:
            item = BudejieItem()
            item['title'] = detail.css('.j-r-list-tool-ct-fx ::attr(data-text)').extract()
            item['content'] = detail.css('.j-r-list-tool-ct-fx ::attr(data-pic)').extract()
            item['preview'] = ''
            item['description'] = detail.css('.j-r-list-c-desc ::text').extract()
            item['classify'] = 'picture'
            if item['title'] and item['content'] and item['preview'] and item['description']:
                items.append(item)
        return items

    def _process_request(self, request):
        # print('process: ' + str(request))
        return request