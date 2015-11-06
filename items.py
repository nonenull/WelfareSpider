# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BedItem(Item):
    title = Field()          # 标题
    description = Field()      # 描述
    preview = Field()      # 缩略图
    content = Field()        # 内容
    classify = Field()       # 分类
    refer = Field()       # 来源