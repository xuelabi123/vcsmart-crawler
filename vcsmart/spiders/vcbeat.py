# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re

class VcbeatSpider(scrapy.Spider):
    name = "vcbeat"
    allowed_domains = ["vcbeat.net"]
    start_urls = ['http://www.vcbeat.net/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@id="article-list"]/div[@class="row phpGetList"]'):
            item = LieyunItem()
            href = div.xpath('div[@class="col-xs-4"]/a/@href').extract()
            img = div.xpath('div[@class="col-xs-4"]/a/img/@src').extract()
            title = div.xpath('div[@class="col-xs-8"]/div/h4/a/text()').extract()
            
            if len(href)==0:
                item['url']=None
            else:
                item['url']= 'http://www.vcbeat.net'+href[0]
                item['title'] = title[0]
                item['img'] = re.sub('/upload/logo','http://www.vcbeat.net/upload/logo',img[0])
                item['source'] = '动脉网'
                item['industry_id'] = 57
                items.append(item)
            
        for item in items:
            if item['url']:
                yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+id="article-content">[\s\S]*?</div>')
        content1 = re.sub('/upload/image','http://www.vcbeat.net/upload/image',content[0])
        tags = response.xpath('//div[@id="tags"]/a/text()').extract()
        item['tags']=[]
        item['content'] = content1
        for tag in tags:
            item['tags'].append(tag)
        return item