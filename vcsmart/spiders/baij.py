# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re


class BaijSpider(scrapy.Spider):
    name = "baij"
    allowed_domains = ["baijingapp.com"]
    start_urls = ['http://www.baijingapp.com/article/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="aw-mod aw-article-list"]/div[@class="ft new-h"]'):
            item = LieyunItem()
            href = div.xpath('dl/dd/div[@class="list-main"]/div[@class="up-box"]/h3/a/@href').extract()
            img = div.xpath('dl/dd/a[@class="post-thumb lazy"]/img/@src').extract()
            title = div.xpath('dl/dd/div[@class="list-main"]/div[@class="up-box"]/h3/a/b/text()').extract()
            
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '白鲸社区'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+id="message".*?>[\s\S]*?</div>')
        pat = re.compile('/ueditor/php/upload')
        result, number = re.subn(pat,'http://www.baijingapp.com/ueditor/php/upload',content[0])
        item['content'] = result
        item['tags']=[]
        return item