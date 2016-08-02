# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HoundItem(scrapy.Item):
    df = scrapy.Field()
    name = scrapy.Field()
    end_flag = scrapy.Field()

class AliListItem(scrapy.Item):
    cate_1       = scrapy.Field()
    cate_2       = scrapy.Field()
    cate_3       = scrapy.Field()
    cate_4       = scrapy.Field()
    cate_5       = scrapy.Field()
    search_count = scrapy.Field()
    item_url     = scrapy.Field()



