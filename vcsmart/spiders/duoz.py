# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class DuozSpider(scrapy.Spider):
    name = "duoz"
    allowed_domains = ["duozhi.com"]
    start_urls = ['http://www.duozhi.com']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="post-list"]/div[@class="post"]'):
            item = LieyunItem()
            href = div.xpath('h3/a/@href').extract()
            img = div.xpath('div[@class="post-content"]/div/a/img/@src').extract()
            title = div.xpath('h3/a/text()').extract()
#            print href,img
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '多知网'
            item['industry_id'] = 1
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="subject-content">[\s\S]*?</div>')
        item['content'] = content[0]
        tags = response.xpath('//div[@class="subject-tags"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item