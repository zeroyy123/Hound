import scrapy
from Hound.items import HoundItem
from bs4 import BeautifulSoup
import pandas as pd
import re

class AliSpider(scrapy.Spider):
    name = "ali"
    allowed_domains = ["aliexpress.com"]

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'ali_apache_id=10.182.248.30.1465380872782.168306.2; aeu_cid=ad789d37373648da87f811228322a4a8-1465380872783-03332-eub6yrrBy; xman_f=1qELjtPKh44N/ddozYt+msbpiqCLzk7oJlMa3PAXow2/eZmyEfcqOPjlZcawdIk+FnMYcRlzBm8o/M5qv5JSrnjON6c9H9Yf3v+XnfO/ECQbbyei8nQXZg==; pgv_pvi=2340168704; ali_beacon_id=120.87.158.138.146450453682.571706.5; cna=uOLFD3o8ymkCAbcxH+wYqBu2; d_ab_f=12a432f7c23548fd903ddacbbf0bd4bd; __utma=3375712.2144992272.1465427270.1467529846.1467632521.7; __utmz=3375712.1465427949.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); acs_usuc_t=acs_rt=166e1da65635431b9e3df363147b842c; xman_t=fZ2pC0gc4NXtbQ8Cg1eTZ68GkSNQNXPdct6kLEk0JlmE/hAYhU/XWK06QW1wexMl; pgv_si=s4093813760; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932640678928; JSESSIONID=F88FC16C0A1A8FCD9B8DF4B6E336D599; alievaluation_ab=183.37.241.254.1465427295406.9; xman_us_f=x_l=0&x_locale=en_US&x_as_i=%7B%22tagtime%22%3A1465380872785%2C%22cn%22%3A%22%22%2C%22cpt%22%3A%221465380872783%22%2C%22affiliateKey%22%3A%22eub6yrrBy%3A%22%2C%22tp1%22%3A%22epn%22%2C%22vd%22%3A%2230%22%2C%22src%22%3A%22aaf%22%2C%22cv%22%3A%225%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22af%22%3A%22735176757%22%7D; intl_locale=en_US; aep_usuc_f=site=glo&region=US&b_locale=en_US&af_tid=ad789d37373648da87f811228322a4a8-1465380872783-03332-eub6yrrBy&c_tp=USD; intl_common_forever=VvvHPuuMt/SYqdN/uFzh/Uya/1giOQ1GBEyT6zMuudSUTSdmlcSVYA==; _mle_tmp0=eNrz4A12DQ729PeL9%2FV3cfUx8KvOTLFScrOwcHM2NHM2cDR0BLJcLJ0sXNxMnMxcjY3NXEwtLZV0kkusDE3MzM0NLS2NTIzNLXQSk9EEciusDGqjAK98GDU%3D; _ga=GA1.2.2144992272.1465427270; ali_apache_track=; ali_apache_tracktmp=; l=Ajc328fPOD4LMcb2w7uUTfxjRyGB/Ate',
        'Host':'www.aliexpress.com',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.640.400 QQBrowser/9.4.8309.400'
    }

    index_df = pd.read_csv('data/item_list.csv')
    def __init__(self, start=0,end=0, *args, **kwargs):
        super(AliSpider, self).__init__(*args, **kwargs)
        print start
        print end
        self.start_urls = (pd.read_csv('data/item_list.csv'))['item_url'].values[int(start):int(end)]  #8:31start

    # print len(start_urls)
    # print start_urls
    # start_urls = [
    #     'http://www.aliexpress.com/category/200003673/daytime-running-lights.html?site=glo&g=y',
    #     'http://www.aliexpress.com/category/200002624/tablet-pc-stands.html?site=glo&shipCountry=all',
    #     # 'http://www.aliexpress.com/category/200084019/wearable-devices.html?site=glo&shipCountry=all',
    #     # 'http://www.aliexpress.com/category/14191206/cable-ties.html?site=glo&shipCountry=all',
    #     # 'http://www.aliexpress.com/category/100006194/pu-er-tea.html?site=glo&shipCountry=all',
    # ]


    def parse(self, response,StartFlag = 1,name='',category='1',son_cate='1',grand_cate='1',gg_son_cate='1'):
        print '#########'
        if StartFlag == 1:
            print 'StartFlag == 1'
            name =  self.index_df[self.index_df['item_url'] == response.url]
            category = (name['catepory'].values)[0]
            son_cate = (name['son_catepory'].values)[0]
            grand_cate =  (name['gra_son_cate'].values)[0]
            gg_son_cate = (name['gg_son_cate'].values)[0]
            name = (name['catepory'].values)[0] + '_' + (name['son_catepory'].values)[0] + '_' + (name['gra_son_cate'].values)[0] + '_' + (name['gg_son_cate'].values)[0]
            name = name.replace(' ','')
            name = name.replace("'",'')
            name = name.replace('&','')
            print name
            # print category,son_cate,grand_cate,gg_son_cate
        # else:
            # print name
            # print category,son_cate,grand_cate,gg_son_cate
        try:
            soup                           = BeautifulSoup(response.body, "html.parser")
            # [category,son_cate,grand_cate] = self.get_relation(soup)
            df                             = self.get_item(soup)
            next_url                       = self.getNextPage(soup)
            print   next_url
        except Exception,e:
            print Exception,":",e

        # print next_url
        item = HoundItem()
        if next_url == 'none':
            item['end_flag'] = 1
        else:

            item['end_flag'] = 0
        try:
            item['name'] = name   ### no data rerurn in the cwarl end ,need to debug
            df['category'] = category
            df['son_cate'] = son_cate
            df['grand_cate'] = grand_cate
            df['gg_son_cate'] = gg_son_cate
            item['df'] = df
        except Exception,e:
            print Exception,":",e
        yield item
        yield scrapy.Request(next_url,headers=self.headers,callback=lambda response,StartFlag=0,\
                                name=name,category=category,son_cate=son_cate,grand_cate=grand_cate,gg_son_cate=gg_son_cate \
                                :self.parse(response,StartFlag,name,category,son_cate,grand_cate,gg_son_cate))

    def getNextPage(self,soup):
        try:
            elems = soup.find_all('a',class_='page-next ui-pagination-next')
            next_url = 'http:'+elems[0].get('href')
            return next_url
        except:
            return 'none'

    def get_relation(self,soup):
        elems = soup.find_all('div',id='aliGlobalCrumb')
        elems = elems[0].find_all('h1')
        a = elems[0].find_all('a')

        if len(a) == 1:
            category = a[0].text
            son_cate = (elems[0].find_all('span'))[1].text
            grand_cate = 'none'
        elif len(a) == 2:
            category = a[0].text
            son_cate = a[1].text
            grand_cate = (elems[0].find_all('span'))[2].text
        else:
            category = a[0].text
            son_cate = a[1].text
            grand_cate = a[2].text+'_'+(elems[0].find_all('span'))[3].text
        return category,son_cate,grand_cate

    def get_item(self,soup):
        try:
            elems = soup.find_all('div',id='main-wrap')
            page_type = elems[0].get('class')
        except Exception,e:
            print Exception,":",e

        if page_type[1] == 'gallery-mode': #'main-wrap gallery-mode'
            return self.get_item_sub1(soup)
        elif page_type[1] == '': #'main-wrap '
            return self.get_item_sub2(soup)
        else:
            print 'none'
            return 'none'

    def get_item_sub1(self,soup):
        results = pd.DataFrame({})
        elems = soup.find_all('div',id='list-items')
        if len(elems) == 0:
            return 'no items'
        elems = elems[0].find_all('li')
        if len(elems) == 0:
            return 'no items'
        print len(elems)
        for i in range(len(elems)):
            elem_ID = elems[i].get('qrdata')
            elem_info = elems[i].find_all('div',class_='info')
            elem_title = elem_info[0].find_all('h3')
            elem_title = elem_title[0].find_all('a')

            elem_price = elem_info[0].find_all('span',class_='value')
            elem_original_price = elem_info[0].find_all('del',class_='original-price')
            elem_order = elem_info[0].find_all('em',title='Total Orders')
            elem_star     = elem_info[0].find_all('span',class_='star star-s')
            elem_feedback = elem_info[0].find_all('a',class_='rate-num ')

            elem_infomore = elems[i].find_all('div',class_='info-more')
            elem_store    = elem_infomore[0].find_all(name='a', attrs={'class':re.compile(r"(store|store j-p4plog)")})

            store_property = elem_infomore[0].find_all('img',class_='score-icon')

            elem_title = elem_title[0].text


            try:
                elem_ship = elem_info[0].find_all('strong')
                if len(elem_ship) != 0:
                    elem_ship = elem_ship[0].text
                else:
                    elem_ship = elem_info[0].find_all('dd',class_='price')
                    if len(elem_ship) != 0:
                        elem_ship = elem_ship[0].text
                    else:
                        elem_ship = 'none'
            except Exception,e:
                print Exception,":",e
                print 'mode 1 elem_ship error'
                elem_ship = 'error'

            try:
                elem_price = elem_price[0].text
            except:
                elem_price = 'none'

            try:
                elem_original_price = elem_original_price[0].text
            except:
                elem_original_price = 'none'

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

            results = results.append(pd.DataFrame({'count':[i],\
                                                            'elem_ID':[elem_ID],\
                                                             'elem_title':[elem_title],\
                                                             'elem_price':[elem_price],\
                                                             'elem_original_price':[elem_original_price],\
                                                             'elem_order':[elem_order],\
                                                             'elem_feedback':[elem_feedback],\
                                                             'elem_star':[elem_star],\
                                                             'elem_store':[elem_store],\
                                                             'store_feedbackscore':[store_feedbackscore],\
                                                             'store_sellerpositivefeedbackpercentage':[store_sellerpositivefeedbackpercentage],\
                                                             'elem_ship':[elem_ship]
                                                            }))
        return results

    def get_item_sub2(self,soup):
        results = pd.DataFrame({})
        elems = soup.find_all('ul',id='list-items')
        if len(elems) == 0:
            return 'no items'

        elems = elems[0].find_all('li')

        if len(elems) == 0:
            return 'no items'
        print len(elems)
        for i in range(len(elems)):
            elem_ID = elems[i].get('qrdata')
            elem_detail = elems[i].find_all('div',class_='detail')
            elem_info   = elems[i].find_all('div',class_='info infoprice')
            elem_title = elem_detail[0].find_all('h3')
            elem_title = elem_title[0].find_all('a')

            elem_price    = elem_info[0].find_all('span',class_='value')
            elem_original_price = elem_info[0].find_all('del',class_='original-price')
            elem_order    = elems[0].find_all('em',title='Total Orders')
            elem_star     = elem_info[0].find_all('span',class_='star star-s')
            elem_feedback = elem_info[0].find_all('a',class_='rate-num ')

            elem_infomore = elems[i].find_all('div',class_='info-more')
            elem_store    = elem_detail[0].find_all(name='a', attrs={'class':re.compile(r"(store|store j-p4plog)")})

            store_property = elem_detail[0].find_all('img',class_='score-icon')

            elem_title = elem_title[0].text

            try:
                elem_ship = elem_info[0].find_all('dd',class_='price')
                # print elem_ship                                                     ## need to debug  why all is freeshiping
                elem_ship = elem_info[0].find_all('strong')
                # print elem_ship
                if len(elem_ship) != 0:
                    elem_ship = elem_ship[0].text
                else:
                    elem_ship = elem_info[0].find_all('dd',class_='price')
                    if len(elem_ship) != 0:
                        elem_ship = elem_ship[0].text
                    else:
                        elem_ship = 'none'
            except Exception,e:
                print Exception,":",e
                print 'mode 2 elem_ship error'
                elem_ship = 'error'

            try:
                elem_price = elem_price[0].text
            except:
                elem_price = 'none'

            try:
                elem_original_price = elem_original_price[0].text
            except:
                elem_original_price = 'none'

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

            results = results.append(pd.DataFrame({'count':[i],\
                                                            'elem_ID':[elem_ID],\
                                                             'elem_title':[elem_title],\
                                                             'elem_price':[elem_price],\
                                                             'elem_original_price':[elem_original_price],\
                                                             'elem_order':[elem_order],\
                                                             'elem_feedback':[elem_feedback],\
                                                             'elem_star':[elem_star],\
                                                             'elem_store':[elem_store],\
                                                             'store_feedbackscore':[store_feedbackscore],\
                                                             'store_sellerpositivefeedbackpercentage':[store_sellerpositivefeedbackpercentage],\
                                                            'elem_ship':[elem_ship]\
                                                            }))
        return results