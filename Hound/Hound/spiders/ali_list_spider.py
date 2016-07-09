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
        if len(elems) == 0:
            print 'start great grand index scanning !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print 'parent url:',response.url
            temp = soup.find_all('div',id='broad-category-main')
            # print len(temp)
            temp = temp[0].find_all('div',id='aliGlobalCrumb')
            temp = temp[0].find_all('h1')
            catepory     = (temp[0].find_all('a'))[0].text
            son_catepory = (temp[0].find_all('span'))[1].text
            # print catepory
            # print son_catepory
            elems = soup.find_all('div',class_='son-bc-list-wrap')
            if len(elems) == 0:
                elems = soup.find_all('div',class_='bc-list-wrap')
            # print len(elems)
            elems = elems[0].find_all('ul',class_='bc-list bc-ul bc-list-not-standard')
            # print 'grand index 1 :',len(elems)
            # print elems
            elems = elems[0].find_all('li',class_='bc-cate-has-child')   ##maybe miss some item which have not child
            # print 'grand index :',len(elems)
            # for elem in elems:
            #     print elem
            for elem in elems:
                gra_son_cate = (elem.find_all('a'))[0].text
                # print gra_son_cate
                sub_elems = elem.find_all('li')
                for sub_elem in sub_elems:
                    print 'Great grand index'
                    print 'parent url:',response.url
                    item_url = 'http:' + sub_elem.find_all('a')[0].get('href')
                    item_name = sub_elem.find_all('a')[0].text
                    print '###gg_son_cate:',item_name
                    item = AliListItem()
                    item['catepory'] = catepory
                    item['son_catepory'] = son_catepory
                    item['gra_son_cate'] = gra_son_cate
                    item['gg_son_cate'] = item_name
                    item['search_count'] = 'none'
                    item['item_url'] = item_url
                    yield item
        else:
            elems = elems[0].find_all('li')
            # print len(elems)
            if len(elems) == 0:
                print 'No grand index'
                print 'parent url:',response.url

                temp = soup.find_all('dl',class_='category-list  ')
                if len(temp) == 0:
                    temp = soup.find_all('dl',class_='category-list  category-list-none-border ')

                if len(temp) == 0:
                    print 'get category-list error'

                catepory = temp[0].find_all('dt',class_='sn-parent-title')
                catepory = catepory[0].find_all('a')
                catepory = catepory[0].text
                catepory = catepory.replace('<','')
                catepory = catepory.replace('\n','')
                catepory = catepory.replace('					','')

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
                item['gg_son_cate'] = 'none'
                item['search_count'] = search_count
                item['item_url'] = item_url
                # print item
                yield item
            else:
                for elem in elems:
                    print 'With grand index'
                    print 'parent url:',response.url

                    temp = soup.find_all('dl',class_='category-list  ')
                    if len(temp) == 0:
                        temp = soup.find_all('dl',class_='category-list  category-list-none-border ')

                    if len(temp) == 0:
                        print 'get category-list error'

                    catepory = temp[0].find_all('dt',class_='sn-parent-title')
                    catepory = catepory[0].find_all('a')
                    catepory = catepory[0].text
                    catepory = catepory.replace('<','')
                    catepory = catepory.replace('\n','')
                    catepory = catepory.replace('					','')

                    temp = temp[0].find_all('dd')
                    # temp = temp[0].find_all('dd')
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
                    item['gg_son_cate'] = 'none'
                    item['search_count'] = search_count
                    item['item_url'] = item_url
                    yield item
