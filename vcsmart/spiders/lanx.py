# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import json
import time

class LanxSpider(scrapy.Spider):
    time_str = str(int(time.time()))
    name = "lanx"
    allowed_domains = ["lanxiongsports.com"]
    start_urls = ['http://www.lanxiongsports.com/mservice/?c=news&a=index&format=json&_='+time_str]

    def parse(self, response):
        news = json.loads(response.body)
#        print news['pager']
        items=[]
        for row in news['items']:
            if row.has_key('position_id'):
                continue
            item = LieyunItem()
            item['url']= 'http://www.lanxiongsports.com/?c=posts&a=view&id='+row['id']
            item['title'] = row['title']
            item['img'] = row['logo']
            item['industry_id'] = 220
            item['source'] = '懒熊体育'
            items.append(item)

            
        for item in items:
            if item['url']:
                yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="top or  imagecontent".*?>[\s\S]*?</div>')
        tags = response.xpath('//div[@class="pag or"]/a/span/text()').extract()
        item['tags']=[]
        item['content'] = content[0]
        for tag in tags:
            item['tags'].append(tag)
        return item