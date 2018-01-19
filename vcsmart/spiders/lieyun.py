# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request
import re

class LieyunSpider(scrapy.Spider):
    name = "lieyun"
    allowed_domains = ["lieyunwang.com"]
    start_urls = ['http://www.lieyunwang.com/archives']

    def parse(self, response):
        items = []
        
        for link in response.xpath("//div[@class='article-box']/ul/li"):
            
            item = LieyunItem()
            href = link.xpath("div[@class='article-info']/a/@href").extract()
            title = link.xpath("div[@class='article-info']/a/text()").extract()
            img = link.xpath("a[@class='article-pic']/img/@data-src").extract()
            type_name = link.xpath("div[@class='article-info']/div/p/span[3]/a[0]").extract()
            item['title'] = title[0]
            item['url'] = 'http://www.lieyunwang.com'+href[0]
            item['img'] = img[0]
            item['source'] = '猎云网'
            if type_name:
                if type_name[0]==u'早期项目':
                    item['type_id']=1
                    item['is_promote']=1
            items.append(item)
            
        for item in items:
            #print item['img']
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class=\"main-text\">[\s\S]*?</div>')
        #print content[0]
        tags = response.xpath('//div[@class="article-tag"]/ul/li/a/text()').extract()
        item['tags']=[]
        pat = re.compile('<span\s+class="poperweima"*?>([\s\S]*?)</span>')
        result, number = re.subn(pat,'',content[0])
        item['content'] = result
        for tag in tags:
            item['tags'].append(tag)
        return item
