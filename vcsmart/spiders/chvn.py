# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class ChvnSpider(scrapy.Spider):
    name = "chvn"
    allowed_domains = ["chinaventure.com.cn"]
    start_urls = ['https://www.chinaventure.com.cn']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="left_list_01"]/ul/li'):
            item = LieyunItem()
            href = div.xpath('div[@class="l_l_01"]/a/@href').extract()
            img = div.xpath('div[@class="l_l_01"]/a/img/@src').extract()
            title = div.xpath('div[@class="l_r_01"]/div[2]/a/text()').extract()
#            print href,img
            item['url']= 'https://www.chinaventure.com.cn'+href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '投资中国'
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<div\s+class="content_01 m_t_30 detasbmo".*?>[\s\S]*?<div>[\s\S]*?</div>[\s\S]*?</div>')
        item['content']=''
        if content:
            item['content'] = content[0]
        tags = response.xpath('//div[@class="lab_01 m_t_40"]/a/text()').extract()
        item['tags']=[]
        for tag in tags:
            item['tags'].append(tag)
        return item