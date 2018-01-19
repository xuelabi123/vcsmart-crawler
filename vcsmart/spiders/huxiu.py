# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = ['https://www.huxiu.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="mod-info-flow"]/div[@class="mod-b mod-art "]'):
            item = LieyunItem()
            href = div.xpath('div[@class="mob-ctt"]/h2/a/@href').extract()
            title = div.xpath('div[@class="mob-ctt"]/h2/a/text()').extract()
            img = div.xpath('div[@class="mod-thumb"]/a/img/@data-original').extract()
            
            item['title'] = title[0]
            item['url'] = 'https://www.huxiu.com'+href[0]
            item['img'] = img[0]
            item['source'] = '虎嗅'
            items.append(item)
            
        for item in items:
            #print item['img']
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        item['content']=None
        content1 = response.xpath('/html/body').re('<div\s+class="article-img-box">[\s\S]*?</div>')
        content2 = response.xpath('/html/body').re('<div\s+id="article_content".*?>[\s\S]*?</div>')
        if len(content1)>0 and len(content2)>0:
            item['content'] = content1[0]+content2[0]
        tags = response.xpath('//div[@class="tag-box "]/ul/a/li/text()').extract()
        item['tags']=[]
        #item['content'] = content1[0]+content2[0]
        for tag in tags:
            item['tags'].append(tag)
        return item