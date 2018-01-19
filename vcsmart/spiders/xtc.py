# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re

class XtcSpider(scrapy.Spider):
    name = "xtc"
    allowed_domains = ["xtecher.com"]
    start_urls = ['http://www.xtecher.com/Website/Article/index']

    def parse(self, response):
        items=[]
        for div in response.xpath('//ul[@class="index_contentList"]/li'):
            item = LieyunItem()
            href = div.xpath('div[@class="index_imgBox"]/a/@href').extract()
            img = div.xpath('div[@class="index_imgBox"]/a/img/@src').extract()
            title = div.xpath('div[@class="leftcontent"]/a/h4/text()').extract()
            
            item['url']='http://www.xtecher.com'+href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = 'Xtecher'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content=''
        content1 = response.xpath('/html/body').re('<div\s+class="content_box".*?>[\s\S]*?</div>')
        content2 = response.xpath('/html/body').re('<div\s+class="content_box feature_content".*?>[\s\S]*?</div>')
        if len(content1)>0:
            content+=content1[0]
        if len(content2)>0:
            content+=content2[0]
        pat = re.compile('/Uploads/Ueditor/image')
        result, number = re.subn(pat,'http://www.xtecher.com/Uploads/Ueditor/image',content)
        item['content'] = result
        item['tags']=[]
        return item