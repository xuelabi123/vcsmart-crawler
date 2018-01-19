# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class CyzSpider(scrapy.Spider):
    name = "cyz"
    allowed_domains = ["cyzone.cn"]
    start_urls = ['http://www.cyzone.cn/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="list-inner"]/div[@class="article-item clearfix"]'):
            item = LieyunItem()
            href = div.xpath('div[@class="item-pic pull-left"]/a/@href').extract()
            img = div.xpath('div[@class="item-pic pull-left"]/a/img/@src').extract()
            title = div.xpath('div[@class="item-intro"]/a/text()').extract()
            
            if len(href)==0:
                item['url']=None
            else:
                item['url']= href[0]
                item['title'] = title[0]
                item['img'] = img[0]
                item['source'] = '创业邦'
                items.append(item)
            
        for item in items:
            if item['url']:
                yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('/html/body').re('<div\s+class="article-content">[\s\S]*?</div>')
        tags = response.xpath('//div[@class="article-tags pull-right"]/a/text()').extract()
        item['tags']=[]
        #item['content'] = content1[0]+content2[0]
        for tag in tags:
            item['tags'].append(tag)
        return item