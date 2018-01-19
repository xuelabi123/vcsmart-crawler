# -*- coding: utf-8 -*-
import scrapy
from vcsmart.items import LieyunItem
from scrapy.http import Request

class BksSpider(scrapy.Spider):
    name = "bks"
    allowed_domains = ["bio4p.com"]
    start_urls = ['http://www.bio4p.com/']

    def parse(self, response):
        items=[]
        for div in response.xpath('//div[@class="articles J_articleList ias_container"]/article'):
            item = LieyunItem()
            href = div.xpath('a[1]/@href').extract()
            img = div.re('http://www.bio4p.com/wp-content/themes/monkey/timthumb.php\?src=.*?q=100')
            title = div.xpath('div[@class="desc"]/a/text()').extract()
            item['url']= href[0]
            item['title'] = title[0]
            item['img'] = img[0]
            item['source'] = '贝壳社'
            item['industry_id'] = 57
            items.append(item)
            
        for item in items:
            yield Request(item['url'], meta={'item':item}, callback=self.parse1)

    def parse1(self, response):
        item = response.meta['item']
        content = response.xpath('/html/body').re('<section\s+class="article">[\s\S]*?<section\s+class="single-post-relate">')
        item['content'] = content[0]
        item['tags']=[]
        return item