# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class CfrjSpider(scrapy.Spider):
    name = "cfrj"
    allowed_domains = ["cunfuriji.com"]
    start_urls = ['http://www.cunfuriji.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="article"]/article'):
            item = LieyunItem()
            href = div.xpath('a[1]/@href').extract()
            img = div.xpath('a[1]/div[1]/img/@src').extract()
            title = div.xpath('header/h2/a/text()').extract()
#            print href,img
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '村夫日记'
            item['industry_id'] = 57
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="post-single-content box mark-links">[\s\S]*?<div\s+class="tags">')
        item['content'] = content[0]
        tags = response.xpath('//div[@class="tags"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item