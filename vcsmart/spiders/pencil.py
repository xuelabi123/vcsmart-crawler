# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class PencilSpider(scrapy.Spider):
    name = "pencil"
    allowed_domains = ["pencilnews.cn"]
    start_urls = ['http://www.pencilnews.cn/info']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@id="artciles_field"]/div[@class="article_block"]'):
            item = LieyunItem()
            href = div.xpath('div[@class="article_img"]/a/@href').extract()
            img = div.xpath('div[@class="article_img"]/a/img/@src').extract()
            title = div.xpath('div[@class="article_content"]/h3/a/text()').extract()
            item['url']='http://www.pencilnews.cn'+href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '铅笔道'
            item['is_promote'] = 1
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item'];
        content=''
        content1 = response.xpath('/html/body').re('<div\s+class="article_digest">[\s\S]*?</div>')
        content2 = response.xpath('/html/body').re('<div\s+class="article_content">[\s\S]*?</div>')
        if len(content1)>0:
            content+=content1[0]
        if len(content2)>0:
            content+=content2[0]
        item['content'] = content
        item['tags']=[]
        return item