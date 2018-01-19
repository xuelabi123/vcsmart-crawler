# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class TmtSpider(scrapy.Spider):
    name = "tmt"
    allowed_domains = ["tmtpost.com"]
    start_urls = ['http://www.tmtpost.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//ul[@class="mod-article-list"]/li'):
            item = LieyunItem()
            href = div.xpath('a[@class="pic"]/@href').extract()
            img = div.xpath('a[@class="pic"]/img/@src').extract()
            title = div.xpath('div[@class="cont"]/h4/a/text()').extract()
            
            if len(href)==0:
                item['url']=None
            else:
                item['url']='http://www.tmtpost.com'+href[0]
                item['title'] = title[0]
                item['img'] = img[0]
                item['source'] = '钛媒体'
                items.append(item)
            
        for item in items:
            if item['url']:
                yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<p\s+class="post-abstract">[\s\S]*?</div>')
#        content2 = response.xpath('/html/body/div[@class="container"]/div[@class="m"]/section/div').re('<div\s+class="inner">[\s\S]*?</div>')
        item['content'] = content[0]
        tags = response.xpath('//div[@class="post-tags"]/span/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item