# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from spider.items import BedItem
from scrapy.spiders import Rule

#居然搞笑网__爬虫
class JuRanSpider(CrawlSpider):
    name = "juran"
    allowed_domains = ["www.zbjuran.com"]
    start_urls = [
        "http://www.zbjuran.com/quweitupian"
    ]
    rules = [
        # 定义爬取URL的规则
        Rule(LinkExtractor(allow=(r"/list_2_\d{0,100000}\.html")), follow=True, callback='parse_item_picture')#图片分类
    ]

    # 处理图片分类，提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item_picture(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.item')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('a b::text').extract()
            item['content'] = detail.css('.text img::attr(src)').extract()
            item['preview'] = ''
            item['description'] = ''
            item['classify'] = 'picture'
            if item['title'] and item['content']:
                items.append(item)
        return items

    def _process_request(self, request):
        print('process: ' + str(request))
        return request