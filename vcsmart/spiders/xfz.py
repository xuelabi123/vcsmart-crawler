# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class XfzSpider(scrapy.Spider):
    name = "xfz"
    allowed_domains = ["xfz.cn"]
    start_urls = ['http://www.xfz.cn']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="content"]/ul/li'):
            item = LieyunItem()
            href = div.xpath('a/@href').extract()
            img = div.xpath('a/div[@class="news-img"]/img/@src').extract()
            title = div.xpath('a/div[@class="news-content"]/div[1]/text()').extract()
#            print href,img
            item['url']= 'http://www.xfz.cn'+href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '小饭桌'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="content-detail">[\s\S]*?</div>')
        item['content'] = content[0]
        item['tags']=[]
        return item