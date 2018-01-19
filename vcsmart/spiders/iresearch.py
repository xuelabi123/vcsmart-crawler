# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class IreSpider(scrapy.Spider):
    name = "ire"
    allowed_domains = ["iresearch.cn"]
    start_urls = ['http://www.iresearch.cn']

    def parse(self, response):
        items=[]
        for div in response.xpath('//ul[@id="htm_box"]/li'):
            item = LieyunItem()
            href = div.re('http://news.iresearch.cn/content/.*?.shtml')
            if href:
                item['url'] = href[0]
            else:
                continue
            img = div.xpath('div[@class="m-item f-cb z-sort-1"]/div[@class="u-img"]/a/img/@src').extract()
            title = div.xpath('div[@class="m-item f-cb z-sort-1"]/div[@class="txt"]/h3/a/text()').extract()
            if title:
                item['title'] = title[0]
            if img:
                item['img'] = img[0]
            item['source'] = '艾瑞网'
            items.append(item)
            
        for item in items:
            #print item['img']
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="m-article">[\s\S]*?<div\s+class="review">[\s\S]*?</div>[\s\S]*?</div>')
        item['content']=content[0]
        tags = response.xpath('//div[@class="tab"]/a/text()').extract()
        item['tags']=[]
        #item['content'] = content1[0]+content2[0]
        for tag in tags:
            item['tags'].append(tag)
        return item