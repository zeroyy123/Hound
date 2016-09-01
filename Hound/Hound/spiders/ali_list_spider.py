import scrapy
from items import AliListItem
from bs4 import BeautifulSoup
import pandas as pd
import re
import copy
from AliList import *

class AliSpider(scrapy.Spider):
    name = "ali_list"
    allowed_domains = ["aliexpress.com"]
    start_urls = [
        'http://www.aliexpress.com/all-wholesale-products.html?spm=2114.01010108.2.2.BiuV4Y',
    ]

    def parse(self, response):
        print '#########'
        top_list = AliList(response)
        [elems_name,elems_parent,elems_url] = top_list.get_top_list()
        L = len(elems_name)
        for i in range(L):
            yield scrapy.Request(elems_url[i], callback=lambda response,cates=[elems_parent[i],elems_name[i]],:self.subParse(response,cates))

    def subParse(self,response,cates):
        List = AliList(response)
        [elems,mode] = List.index_mode_adjust()
        if mode ==  'list mode':
            elems = List.get_li_listmode(elems)
            if len(elems) == 0:
                [item_name,item_url,search_count] = List.get_item_detial()
                cates_sub = copy.copy(cates)
                cates_sub.append(item_name)
                print 'end node'
                print cates_sub
                print 'search_count: ',search_count
                print 'category length: ',len(cates_sub)
                print item_url
                item = AliListItem()
                for i in range(5):
                    temp = 'cate_'+str(i+1)
                    if (i+1) < len(cates_sub):
                        item[temp] = cates_sub[i]
                    else:
                        item[temp] = ''
                item['search_count'] = search_count
                item['item_url'] = item_url
                yield item
            else:
                for elem in elems:
                    [item_name,item_url] = List.get_next_url(elem)
                    cates_sub = copy.copy(cates)
                    cates_sub.append(item_name)
                    yield scrapy.Request(item_url, callback=lambda response,cates=cates_sub,:self.subParse(response,cates))
        elif mode ==  'broad mode':
            [items_name,items_url,items_parent] = List.get_li_detial_boardmode()
            for i in range(len(items_name)):
                cates_sub = copy.copy(cates)
                if items_parent[i] != '':
                    cates_sub.append(items_parent[i])
                cates_sub.append(items_name[i])
                yield scrapy.Request(items_url[i], callback=lambda response,cates=cates_sub,:self.subParse(response,cates))
        else:
            print 'mode adjust error'
