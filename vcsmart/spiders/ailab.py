# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class AilabSpider(scrapy.Spider):
    name = "ailab"
    allowed_domains = ["ailab.cn"]
    start_urls = ['http://www.ailab.cn']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="col-left box mt10"]/ul/li'):
            item = LieyunItem()
            href = div.xpath('a[1]/@href').extract()
            img = div.xpath('a[1]/img/@src').extract()
            title = div.xpath('a[2]/text()').extract()
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '人工智能网'
            item['industry_id'] = 545
            items.append(item)
            
        for item in items:
#            pass
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content_p = response.xpath('//div[@class="content_z"]/p').extract()
        content_p.remove(content_p[0])
        content=''
        for p in content_p:
            content += p
        item['content'] = content
        tags = response.xpath('//p[@class="p arckw"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item