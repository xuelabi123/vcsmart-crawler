# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re

class YienSpider(scrapy.Spider):
    name = "yien"
    allowed_domains = ["entgroup.cn"]
    start_urls = ['http://www.entgroup.cn/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="main"]/div[@class="articlebox"]'):
            item = LieyunItem()
            href = div.xpath('div[@class="imgbox imgbox01"]/a[2]/@href').extract()
            img = div.xpath('div[@class="imgbox imgbox01"]/a[2]/img/@src').extract()
            title = div.xpath('div[@class="contbox"]/h1/a/text()').extract()
#            print href,img
            item['url']= 'http://www.entgroup.cn'+href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '艺恩网'
            item['industry_id'] = 119
            items.append(item)
            
        for item in items:
#            pass
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="detailsbox">[\s\S]*?<div\s+class="zhaiyao">[\s\S]*?<div>[\s\S]*?</div>[\s\S]*?</div>[\s\S]*?</div>')
        content1 = re.sub(r'<h1.*?>[\s\S]*?</h1>','',content[0])
        content2 = re.sub(r'<div\s+class="biaoqian">[\s\S]*?</div>','',content1)
        item['content'] = content2
        tags = response.xpath('//div[@class="biaoqian"]/span[1]/a/text()').extract()
        item['tags']=[]
        #item['content'] = content1[0]+content2[0]
        for tag in tags:
            item['tags'].append(tag)
        return item