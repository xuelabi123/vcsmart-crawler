# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class YiouSpider(scrapy.Spider):
    name = "yiou"
    allowed_domains = ["iyiou.com"]
    start_urls = ['http://www.iyiou.com/newpost']

    def parse(self, response):
        items=[]
        for div in response.xpath('//ul[@class="specificpost-list"]/li'):
            item = LieyunItem()
            href = div.xpath('div[@class="img fl"]/a/@href').extract()
            img = div.xpath('div[@class="img fl"]/a/img/@src').extract()
            title = div.xpath('div[@class="text fl"]/a/h2/text()').extract()
            
            item['title'] = title[0]
            item['url'] = href[0]
            item['img'] = img[0]
            item['source'] = '亿欧'
            items.append(item)
            
        for item in items:
            #print item['img']
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        item['content']=''
        content1 = response.xpath('/html/body').re('<div\s+id="post_brief">[\s\S]*?</div>')
        content2 = response.xpath('/html/body').re('<div\s+id="post_thumbnail">[\s\S]*?</div>')
        content3 = response.xpath('/html/body').re('<div\s+id="post_description">[\s\S]*?</div>')
        if len(content1)>0:
            item['content']+=content1[0]
        if len(content2)>0:
            item['content']+=content2[0]
        if len(content3)>0:
            item['content']+=content3[0]
        tags = response.xpath('//div[@class="article_info_box_right"]/a/text()').extract()
        item['tags']=[]
        #item['content'] = content1[0]+content2[0]
        for tag in tags:
            item['tags'].append(tag)
        return item