# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class ZhidxSpider(scrapy.Spider):
    name = "zhidx"
    allowed_domains = ["zhidx.com"]
    start_urls = ['http://zhidx.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="tabCont tabCont1"]/ul/li'):
            item = LieyunItem()
            href = div.xpath('a[@class="img"]/@href').extract()
            img = div.xpath('a[@class="img"]/img/@src').extract()
            title = div.xpath('p[@class="name"]/a/text()').extract()
            
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '智东西'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="finCnt">[\s\S]*?</div>')
        pat = re.compile('<script\s+.*?>[\s\S]*</script>')
        result, number = re.subn(pat,'',content)
        
        item['content'] = result
        tags = response.xpath('//em[@class="leibie"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item