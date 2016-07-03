import scrapy
from Hound.items import AliListItem
from bs4 import BeautifulSoup
import pandas as pd
import re

class AliSpider(scrapy.Spider):
    name = "ali_list"
    allowed_domains = ["aliexpress.com"]
    start_urls = [
        'http://www.aliexpress.com/all-wholesale-products.html?spm=2114.01010108.2.2.BiuV4Y',
    ]

    def parse(self, response):
        print '#########'
        soup = BeautifulSoup(response.body, "html.parser")
        elems = soup.find_all('div',class_='cg-main')
        elems = elems[0].find_all('li')
        # print len(elems)
        for elem in elems:
            elem = elem.find_all('a')
            elem_url = 'http:' + elem[0].get('href')
            print elem_url
            print elem[0].text
            yield scrapy.Request(elem_url, callback=self.subParse)

    def subParse(self,response):
        soup = BeautifulSoup(response.body, "html.parser")
        elems = soup.find_all('dl',class_='son-category')
        elems = elems[0].find_all('li')
        # print len(elems)
        if len(elems) == 0:
            temp = soup.find_all('dl',class_='category-list  ')
            temp = temp[0].find_all('dt',class_='sn-parent-title')
            temp = temp[0].find_all('a')
            catepory = temp[0].text
            catepory = catepory.replace('<','')
            catepory = catepory.replace('\n','')
            catepory = catepory.replace('					','')

            temp = soup.find_all('dl',class_='category-list  ')
            temp = temp[0].find_all('dd')
            temp = temp[0].find_all('dd')
            if len(temp[0].find_all('dd')) == 0:
                # print '********'
                temp = temp[0].find_all('dt',class_='sn-parent-title')
                temp = temp[0].find_all('span')
                son_catepory = temp[0].text
            else:
                # print '#########'
                temp = temp[0].find_all('dd')
                temp = temp[0].find_all('dt',class_='sn-parent-title')
                temp = temp[0].find_all('span')
                son_catepory = temp[0].text

            temp = soup.find_all('strong',class_='search-count')
            search_count = temp[0].text
            gra_son_cate = 'none'

            item_url = response.url

            item = AliListItem()
            item['catepory'] = catepory
            item['son_catepory'] = son_catepory
            item['gra_son_cate'] = gra_son_cate
            item['search_count'] = search_count
            item['item_url'] = item_url
            yield item
        else:
            for elem in elems:
                # print '$$$$$$$$$'
                # print 'parent url:',response.url
                temp = soup.find_all('dl',class_='category-list  ')
                temp = temp[0].find_all('dt',class_='sn-parent-title')
                temp = temp[0].find_all('a')
                catepory = temp[0].text
                catepory = catepory.replace('<','')
                catepory = catepory.replace('\n','')
                catepory = catepory.replace('					','')

                temp = soup.find_all('dl',class_='category-list  ')
                temp = temp[0].find_all('dd')
                temp = temp[0].find_all('dd')
                if len(temp[0].find_all('dd')) == 0:
                    # print '********'
                    temp = temp[0].find_all('dt',class_='sn-parent-title')
                    temp = temp[0].find_all('span')
                    son_catepory = temp[0].text
                else:
                    # print '#########'
                    temp = temp[0].find_all('dd')
                    temp = temp[0].find_all('dt',class_='sn-parent-title')
                    temp = temp[0].find_all('span')
                    son_catepory = temp[0].text

                temp = elem.find_all('a')
                gra_son_cate = temp[0].text

                temp = elem.find_all('span')
                search_count = temp[0].text

                temp = elem.find_all('a')
                item_url = 'http:' + temp[0].get('href')

                item = AliListItem()
                item['catepory'] = catepory
                item['son_catepory'] = son_catepory
                item['gra_son_cate'] = gra_son_cate
                item['search_count'] = search_count
                item['item_url'] = item_url
                yield item
