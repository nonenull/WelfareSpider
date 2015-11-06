# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import MySQLdb

class checkItemAndSaveItem(object):
    def __init__(self):
        try:
            self.conn= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='',db ='bed')
            self.cur = self.conn.cursor()
            print "Mysql连接成功"
        except Exception as e:
            print "Mysql连接失败",e

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        classify = item['classify']
        refer = item['refer']
        preview = item['preview']
        description = item['description']
        if isinstance(title,list):
            title = item['title'][0]
        if isinstance(content,list):
            content = item['content'][0]
        if isinstance(preview,list):
            preview = item['preview'][0]
        if isinstance(description,list):
            description = item['description'][0]
        if self.check_duplicate(title):
            #preview 存在是picture分类
            sql = 'insert into bed_content(title,description,preview,content,classify,refer,createTime)value("%s","%s","%s","%s","%s","%s",now())'%(title,description,preview,content,classify,refer)
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print sql,e
            return item
        else:
            raise DropItem("Missing title or content in %s" % title[i])

    # def process_item(self, item, spider):
    #     title = item['title']
    #     content = item['content']
    #     classify = item['classify']
    #     preview = item['preview']
    #     description = item['description']
    #     num = xrange(len(title))
    #     for i in num:
    #         if title[i] and content[i]:
    #             title[i] = title[i].strip()
    #             if self.check_duplicate(title[i]):
    #                 #preview 存在是picture分类
    #                 if preview:
    #                     sql = 'insert into bed_content(title,description,preview,content,classify,createTime)value("%s","%s","%s","%s","%s",now())'%(title[i],description[i].strip(),preview[i],content[i],classify)
    #                 else:
    #                     #text分类
    #                     sql = 'insert into bed_content(title,content,classify,createTime)value("%s","%s","%s",now())'%(title[i],content[i].strip(),classify)
    #                 try:
    #                     self.cur.execute(sql)
    #                     self.conn.commit()
    #                 except Exception as e:
    #                     print sql,e
    #                 return item
    #         else:
    #             raise DropItem("Missing title or content in %s" % title[i])


    #检查内容是否有重复
    def check_duplicate(self,title):
        sql = 'select count(1) from bed_content where title="%s"'%(title)
        self.cur.execute(sql)
        #如果有重复返回FALSE，否则True
        if self.cur.fetchone()[0] > 0:
            return False
        return True

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()
