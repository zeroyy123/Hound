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
    catepory     = scrapy.Field()
    son_catepory = scrapy.Field()
    gra_son_cate = scrapy.Field()
    search_count = scrapy.Field()
    item_url     = scrapy.Field()



