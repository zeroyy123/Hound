import scrapy
from Hound.items import HoundItem
from bs4 import BeautifulSoup
import pandas as pd
import re

class AliSpider(scrapy.Spider):
    name = "ali"
    allowed_domains = ["aliexpress.com"]
    start_urls = [
        'http://www.aliexpress.com/category/200000707/tops-tees.html?spm=2114.11010108.102.3.azoeiz&g=y',
        # 'http://www.aliexpress.com/category/200001648/blouses-shirts.html?g=y'
    ]
    page_counter = 0
    results = pd.DataFrame({})

    def parse(self, response):
        print '#########'
        soup = BeautifulSoup(response.body, "html.parser")
        self.results = pd.DataFrame({})
        self.get_item(soup)
        next_url = self.getNextPage(soup)

        # print next_url

        elems = soup.find_all('div',id='aliGlobalCrumb')
        elems = elems[0].find_all('h1')
        category = (elems[0].find_all('a'))[0].text
        item_name = (elems[0].find_all('span'))[1].text

        if category == " Men's Clothing & Accessories":
            self.page_counter = self.page_counter + 1

        print self.page_counter

        print category
        print item_name

        item = HoundItem()
        if next_url == 'none':
            item['end_flag'] = 1
        else:
            item['end_flag'] = 0

        item['category'] = category
        item['item_name'] = item_name
        item['df'] = self.results
        yield item
        yield scrapy.Request(next_url, callback=self.parse)

    def getNextPage(self,soup):
        try:
            elems = soup.find_all('a',class_='page-next ui-pagination-next')
            next_url = 'http:'+elems[0].get('href')
            return next_url
        except:
            return 'none'

    def get_item(self,soup):
        try:
            elems = soup.find_all('div',id='main-wrap')
            page_type = elems[0].get('class')
            print page_type[0]
        except Exception,e:
            print Exception,":",e


        if len(page_type) == 2: #'main-wrap gallery-mode'
            return self.get_item_sub1(soup)
        elif len(page_type) == 1: #'main-wrap '
            return self.get_item_sub2(soup)
        else:
            print 'none'
            return 'none'

    def get_item_sub1(self,soup):
        elems = soup.find_all('div',id='list-items')
        if len(elems) == 0:
            return 'no items'
        elems = elems[0].find_all('li')
        if len(elems) == 0:
            return 'no items'
        print len(elems)
        for i in range(len(elems)):
            elem_info = elems[i].find_all('div',class_='info')
            elem_title = elem_info[0].find_all('h3')
            elem_title = elem_title[0].find_all('a')

            elem_price = elem_info[0].find_all('span',class_='value')
            elem_order = elem_info[0].find_all('em',title='Total Orders')
            elem_star     = elem_info[0].find_all('span',class_='star star-s')
            elem_feedback = elem_info[0].find_all('a',class_='rate-num ')

            elem_infomore = elems[i].find_all('div',class_='info-more')
            elem_store    = elem_infomore[0].find_all(name='a', attrs={'class':re.compile(r"(store|store j-p4plog)")})

            store_property = elem_infomore[0].find_all('img',class_='score-icon')

            elem_title = elem_title[0].text

            try:
                elem_price = elem_price[0].text
            except:
                elem_price = 'none'

            try:
                elem_order = elem_order[0].text
            except:
                elem_order = 'none'

            try:
                elem_star = elem_star[0].get('title')
            except:
                elem_star = 'none'

            try:
                elem_feedback = elem_feedback[0].text
            except:
                elem_feedback = '(0)'

            try:
                elem_store = elem_store[0].get('title')
            except:
                elem_store = 'none'

            try:
                store_feedbackscore = store_property[0].get('feedbackscore')
                store_sellerpositivefeedbackpercentage = store_property[0].get('sellerpositivefeedbackpercentage')
            except:
                store_feedbackscore = 'none'
                store_sellerpositivefeedbackpercentage = 'none'

            self.results = self.results.append(pd.DataFrame({'count':[i],\
                                                             'elem_title':[elem_title],\
                                                             'elem_price':[elem_price],\
                                                             'elem_order':[elem_order],\
                                                             'elem_feedback':[elem_feedback],\
                                                             'elem_star':[elem_star],\
                                                             'elem_store':[elem_store],\
                                                             'store_feedbackscore':[store_feedbackscore],\
                                                             'store_sellerpositivefeedbackpercentage':[store_sellerpositivefeedbackpercentage]}))
        return 'success'

    def get_item_sub2(self,soup):
        elems = soup.find_all('ul',id='list-items')

        if len(elems) == 0:
            return 'no items'

        elems = elems[0].find_all('li')

        if len(elems) == 0:
            return 'no items'
        print len(elems)
        for i in range(len(elems)):
            elem_detail = elems[i].find_all('div',class_='detail')
            elem_info   = elems[i].find_all('div',class_='info infoprice')
            elem_title = elem_detail[0].find_all('h3')
            elem_title = elem_title[0].find_all('a')

            elem_price    = elem_info[0].find_all('span',class_='value')
            elem_order    = elems[0].find_all('em',title='Total Orders')
            elem_star     = elem_info[0].find_all('span',class_='star star-s')
            elem_feedback = elem_info[0].find_all('a',class_='rate-num ')

            elem_infomore = elems[i].find_all('div',class_='info-more')
            elem_store    = elem_detail[0].find_all(name='a', attrs={'class':re.compile(r"(store|store j-p4plog)")})

            store_property = elem_detail[0].find_all('img',class_='score-icon')

            elem_title = elem_title[0].text

            try:
                elem_price = elem_price[0].text
            except:
                elem_price = 'none'

            try:
                elem_order = elem_order[0].text
            except:
                elem_order = 'none'

            try:
                elem_star = elem_star[0].get('title')
            except:
                elem_star = 'none'

            try:
                elem_feedback = elem_feedback[0].text
            except:
                elem_feedback = '(0)'

            try:
                elem_store = elem_store[0].get('title')
            except:
                elem_store = 'none'

            try:
                store_feedbackscore = store_property[0].get('feedbackscore')
                store_sellerpositivefeedbackpercentage = store_property[0].get('sellerpositivefeedbackpercentage')
            except:
                store_feedbackscore = 'none'
                store_sellerpositivefeedbackpercentage = 'none'

            self.results = self.results.append(pd.DataFrame({'count':[i],\
                                                             'elem_title':[elem_title],\
                                                             'elem_price':[elem_price],\
                                                             'elem_order':[elem_order],\
                                                             'elem_feedback':[elem_feedback],\
                                                             'elem_star':[elem_star],\
                                                             'elem_store':[elem_store],\
                                                             'store_feedbackscore':[store_feedbackscore],\
                                                             'store_sellerpositivefeedbackpercentage':[store_sellerpositivefeedbackpercentage]}))
        return 'success'