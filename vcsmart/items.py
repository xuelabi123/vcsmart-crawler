# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LieyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    industry_id = scrapy.Field()
    type_id = scrapy.Field()
    is_promote = scrapy.Field()
    publish_time = scrapy.Field()
