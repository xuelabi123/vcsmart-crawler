# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class LeifSpider(scrapy.Spider):
    name = "leif"
    allowed_domains = ["leiphone.com"]
    start_urls = ['http://www.leiphone.com']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="lph-pageList index-pageList"]/div[@class="list"]/ul/li'):
            item = LieyunItem()
            href = div.xpath('div/div[@class="img"]/a[2]/@href').extract()
            img = div.xpath('div/div[@class="img"]/a[2]/img/@data-original').extract()
            title = div.xpath('div/div[@class="word"]/h3/a/text()').extract()
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '雷锋网'
            items.append(item)
            
        for item in items:
#            pass
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="lph-article-comView">[\s\S]*?</div>')
        item['content'] = content[0]
        tags = response.xpath('//div[@class="related-link clr"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item