# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re

class GgmtSpider(scrapy.Spider):
    name = "ggmt"
    allowed_domains = ["svinsight.com"]
    start_urls = ['http://www.svinsight.com']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="col-md-9 wleft"]/div[@class="media read"]'):
            item = LieyunItem()
            href = div.xpath('div[@class="media-left"]/div/a/@href').extract()
            img = div.re('url\(.*?\)')
            img1 = re.sub('(url\()|(\))','',img[0])
            title = div.xpath('div[@class="media-body"]/a/h4/text()').extract()
            item['url']= 'http://www.svinsight.com'+href[0]
#            print title
            item['title'] = title[0]
            item['img'] = img1
            item['source'] = '硅谷密探'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content_p = response.xpath('//div[@class="wb"]/p').extract()
        content=''
        for p in content_p:
            content += p
        item['content'] = content
        tags = response.xpath('//div[@class="wb"]/div[2]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item