# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class JmtSpider(scrapy.Spider):
    name = "jmt"
    allowed_domains = ["jingmeiti.com"]
    start_urls = ['http://www.jingmeiti.com/?cat=5']

    def parse(self, response):
        items=[]
        for div in response.xpath('//ul[@class="article-list"]/li'):
            item = LieyunItem()
            href = div.xpath('div[@class="fl"]/a/@href').extract()
            img = div.xpath('div[@class="fl"]/a/img/@src').extract()
            title = div.xpath('div[@class="info"]/div[@class="art-tit"]/a/text()').extract()
            
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '鲸媒体'
            item['industry_id'] = 1
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="art-con">[\s\S]*?</div>')
        item['content'] = content[0]
        tags = response.xpath('//div[@class="article-tag"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item