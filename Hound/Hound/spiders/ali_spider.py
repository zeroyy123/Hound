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
        'http://www.aliexpress.com/category/14191299/other-wiring-accessories.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191209/wiring-ducts.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190402/electrical-wires.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410605/push-button-switches.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/141909/relays.html',
        'http://www.aliexpress.com/category/14191208/tie-mounts.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190499/other-wires-cables-cable-assemblies.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/141907/transformers.html',
        'http://www.aliexpress.com/category/14191102/inverters-converters.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410606/remote-control-switches.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191203/cable-end-caps.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410401/alternative-energy-generators.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/540/fuses.html',
        'http://www.aliexpress.com/category/4103/fuse-components.html',
        'http://www.aliexpress.com/category/150512/electronic-instrument-enclosures.html',
        'http://www.aliexpress.com/category/141905/electrical-plugs-sockets.html',
        'http://www.aliexpress.com/category/14190409/power-cords-extension-cords.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191101/ac-dc-adapters.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410612/wall-switches.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191207/cable-trays.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410405/generator-parts-accessories.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190404/cable-manufacturing-equipment.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/526/contactors.html',
        'http://www.aliexpress.com/category/14190101/connectors.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191104/switching-power-supply.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410607/rocker-switches.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410403/gasoline-generators.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190410/wiring-harness.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190103/terminals.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191105/inductors.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410603/limit-switches.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/410402/diesel-generators.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190408/power-cables.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14190199/other-connectors-terminals.html?site=glo&shipCountry=all',
        'http://www.aliexpress.com/category/14191107/voltage-regulators-stabilizers.html?site=glo&shipCountry=all'


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