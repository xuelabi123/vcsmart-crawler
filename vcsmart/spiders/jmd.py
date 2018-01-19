# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class JmdSpider(scrapy.Spider):
    name = "jmd"
    allowed_domains = ["jiemodui.com"]
    start_urls = ['https://www.jiemodui.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@id="news"]/dl'):
            item = LieyunItem()
            href = div.xpath('dt/a/@href').extract()
            img = div.re(r'https://[\s\S]*?320_240.jpg')
            title = div.xpath('dd/h3/a/text()').extract()
            item['url']= 'https://www.jiemodui.com'+href[0]
            item['title'] = title[0]
            if img:
                item['img'] = img[0]
            else:
                item['img'] = ''
            item['source'] = '芥末堆'
            item['industry_id'] = 1
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<article\s+class="content">[\s\S]*?</div>')
        tags = response.xpath('//ul[@id="Mocs_lis"]/li/a/text()').extract()
        item['tags']=[]
        item['content'] = content[0]
        for tag in tags:
            item['tags'].append(tag)
        return item