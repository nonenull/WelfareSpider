# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from spider.items import BedItem
from scrapy.spiders import Rule,Request
import time

#搞笑啦__爬虫
class GaoXiaoLaSpider(CrawlSpider):
    name = "gaoxiaola"
    allowed_domains = ["www.gaoxiaola.com"]
    start_urls = [
        "http://www.gaoxiaola.com/gif/"

    ]
    rules = [
        # 定义爬取URL的规则
        # Rule(LinkExtractor(allow=(r"[a-z]{0,10}/$")), follow=True, callback='parse_item_video'),#视频分类
        Rule(LinkExtractor(allow=(r"[a-z]{0,10}.html")), follow=True, callback='parse_item_picture')#图片分类
    ]

    # 处理视频分类，提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item_video(self, response):
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('li[class="coments"]')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.m_v_list_txt a::text').extract()
            item['preview'] = detail.css('a img::attr(src)').extract()
            item['description'] = ''
            item['classify'] = 'video'
            video_url = detail.css('a ::attr(href)').extract()[0]
            video_content = Request(video_url)
            video_sel = Selector(video_content)
            item['content'] = video_sel.css('.video-bar a::attr(href)').extract()
            if item['title'] and item['content']:
                items.append(item)
        return items

    # 处理图片分类，提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item_picture(self, response):
        time.sleep(3)
        items = []
        sel = Selector(response)
        #获取标题，内容，预览图,描述
        detail_div = sel.css('.con')
        for detail in detail_div:
            item = BedItem()
            item['title'] = detail.css('.head .title::text').extract()
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