# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import spider_class as spc
import numpy as np

class spider_aliexp(spc.spider):

    def open_web_url(self,url):
        if url == '':
            url = "http://www.aliexpress.com"
        self.driver.get(url)

    def get_index(self):
        root_path = '//dl[@data-role="first-menu"]'
        cate_name_path = '/dt/span'
        sub_root_path  = '/dd/div[@class="sub-cate-main"]/div[@class="sub-cate-row"]'
        sub_cate_column_path = '/dl'
        sub_cate_name_path = '/dt/a'
        sub_cate_item_path = '/dd/a'

        cate_num = len(self.driver.find_elements_by_xpath(root_path))
        df = pd.DataFrame({})
        for i in range(cate_num):
            n = i + 1
            elem = self.driver.find_elements_by_xpath(root_path + '['+str(n)+']'+cate_name_path)
            ActionChains(self.driver).move_to_element(elem[0]).perform()
            time.sleep(2)
            cate_name = elem[0].text
            print cate_name

            sub_cate_row = len(self.driver.find_elements_by_xpath(root_path + '['+str(n)+']' + sub_root_path))
            # print sub_cate_row
            for j in range(sub_cate_row):
                m = j + 1
                sub_cate_column = len(self.driver.find_elements_by_xpath(root_path + '['+str(n)+']'+sub_root_path + '['+str(m)+']' + sub_cate_column_path))
                # print sub_cate_column
                for k in range(sub_cate_column):
                    o = k + 1
                    sub_cate_name = self.driver.find_elements_by_xpath(root_path + '['+str(n)+']'+sub_root_path + '['+str(m)+']' \
                                                                       + sub_cate_column_path + '['+str(o)+']' + sub_cate_name_path)
                    sub_cate_name = sub_cate_name[0].text
                    print ' ',sub_cate_name
                    sub_cate_item = self.driver.find_elements_by_xpath(root_path + '['+str(n)+']'+sub_root_path + '['+str(m)+']' \
                                                                       + sub_cate_column_path + '['+str(o)+']' + sub_cate_item_path)
                    for item in sub_cate_item:
                        item_name = item.text
                        url = item.get_attribute('href')
                        df = df.append(pd.DataFrame({'category':[cate_name],'sub_cate':[sub_cate_name],'item':[item_name],'url':[url]}))
                        print '     ',item_name
        print df
        df.to_csv('ali_cate_list.csv',encoding='utf-8')
        return df

    def search_item(self,target):
        search_key = target
        elems = self.driver.find_elements_by_xpath('//div[@class="search-key-box"]/input[@type="text"]')
        ##print len(elems)
        elems[0].send_keys(Keys.BACKSPACE + search_key + Keys.RETURN)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1)

    def get_search_count(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="search-result"]//strong[@class="search-count"]')
        print self.driver.title
        try:
            result = elems[0].text
        except:
            result = 'none'
        return result

    def get_page_num(self):

        elems = self.driver.find_elements_by_xpath('//span[@id="pagination-max"]')
        try:
            page_num = int(elems[0].get_attribute('innerHTML'))
            return page_num
        except:
            return 1

    def get_item(self):
        try:
            page_type = self.driver.find_elements_by_xpath('//div[@id="main-wrap"]')[0].get_attribute('class')
        except:
            return 'error'
        # print page_type
        if page_type == 'main-wrap gallery-mode':
            print page_type
            xpath_root = '//div[@id="list-items"]/ul/li'
        elif page_type == 'main-wrap ':
            print page_type
            xpath_root = '//div[@id="main-wrap"]/ul[@id="list-items"]/li'
        else:
            print 'error unknow page type'

        elems = self.driver.find_elements_by_xpath(xpath_root)
        num = len(elems)

        if num == 0:
            url = self.driver.current_url
            self.driver.get(url)
            time.sleep(1)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(1)
            js="var q=document.body.scrollTop=10000"
            self.driver.execute_script(js)

            elems = self.driver.find_elements_by_xpath(xpath_root)
            num = len(elems)
        print num

        if page_type == 'main-wrap gallery-mode':
            return self.get_item_sub1()
        elif page_type == 'main-wrap ':
            return self.get_item_sub2()
        else:
            print 'none'
            return 'none'
##

    def get_item_sub1(self):
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")

        elems = soup.find_all('div',id='list-items')
        if len(elems) == 0:
            return 'no items'

        elems = elems[0].find_all('li')
        if len(elems) == 0:
            return 'no items'

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

    def get_item_sub2(self):
        response = self.driver.page_source
        soup = BeautifulSoup(response, "html.parser")

        elems = soup.find_all('ul',id='list-items')

        if len(elems) == 0:
            return 'no items'

        elems = elems[0].find_all('li')

        if len(elems) == 0:
            return 'no items'

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

    def go_page(self,page):
        elems = self.driver.find_elements_by_xpath('//input[@id="pagination-bottom-input"]')
        elems[0].send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + str(page))
        elems[0].send_keys(Keys.RETURN)

        time.sleep(0.5)
        js="var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)

    def next_page(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="ui-pagination-navi util-left"]/a[@class = "page-next ui-pagination-next"]')
        elems[0].click()
        time.sleep(0.5)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(0.5)

    def data_reduction(self):
        index_table = pd.read_csv('data/ali_cate_list.csv')
        L = len(index_table)
        df = pd.DataFrame({})
        category = ''
        for n in range(L):
            Last_category = category
            category = index_table['category'].values[n]
            category = category.replace("’","'")
            sub_cate = index_table['sub_cate'].values[n]
            sub_cate = sub_cate.replace("’","'")
            item = index_table['item'].values[n]
            item = item.replace("’","'")
            
            target = category + '_' + sub_cate + '_' + item
            # target = target.replace("'","")
            try:
                data = pd.read_csv('data/'+target+'.csv')
                del data['Unnamed: 0']
                L_1 = len(data)
                print target,L_1

                data['sub_cate'] = sub_cate
                data['item']     = item
                
                elem_feedback        = data['elem_feedback'].values
                elem_order           = data['elem_order'].values
                elem_price           = data['elem_price'].values
                elem_price_low       = elem_price.copy()  # shallow copy ,(deepcopy() for deep copy)
                elem_price_high      = elem_price.copy()
                elem_star            = data['elem_star'].values
                store_feedbackscore  = data['store_feedbackscore'].values
                store_sellerpositivefeedbackpercentage = data['store_sellerpositivefeedbackpercentage'].values
            
                for i in range(L_1):
                    if elem_feedback[i]=='none':
                        elem_feedback[i] = np.nan
                    else:
                        elem_feedback[i] = elem_feedback[i].replace('Feedback','')
                        elem_feedback[i] = elem_feedback[i].replace('(','')
                        elem_feedback[i] = int(elem_feedback[i].replace(')',''))
                        
                    if elem_order[i]=='none':
                        elem_order[i] = np.nan
                    else:
                        elem_order[i] = elem_order[i].replace('Orders  (','')
                        elem_order[i] = elem_order[i].replace('Orders (','')
                        elem_order[i] = elem_order[i].replace('Order  (','')
                        elem_order[i] = elem_order[i].replace('Order (','')
                        elem_order[i] = int(elem_order[i].replace(')',''))

                    if elem_price[i]=='none':
                        elem_price_low[i] = np.nan
                        elem_price_high[i] = np.nan
                    else:
                        elem_price[i] = elem_price[i].replace('US $','')
                        elem_price[i] = elem_price[i].replace(',','')
                        if elem_price[i].find(' - ') == -1:
                            elem_price_low[i]  = float(elem_price[i])
                            elem_price_high[i] = float(elem_price[i])
                        else:
                            elem_price_temp = elem_price[i].split(' - ')
                            elem_price_low[i]  = float(elem_price_temp[0])
                            elem_price_high[i] = float(elem_price_temp[1])

                            
                    if elem_star[i]=='none':
                        elem_star[i] = np.nan
                    else:
                        elem_star[i] = elem_star[i].replace('Star Rating: ','')
                        elem_star[i] = float(elem_star[i].replace(' out of 5',''))
                        
                    if store_feedbackscore[i]=='none':
                        store_feedbackscore[i] = np.nan
                    else:
                        store_feedbackscore[i] = store_feedbackscore[i].replace(',','')
                        store_feedbackscore[i] = int(store_feedbackscore[i])
                        
                    if store_sellerpositivefeedbackpercentage[i]=='none':
                        store_sellerpositivefeedbackpercentage[i] = np.nan
                    else:
                        store_sellerpositivefeedbackpercentage[i] = float(store_sellerpositivefeedbackpercentage[i])
        
                data['elem_feedback']           = elem_feedback
                data['elem_order']              = elem_order
                data['elem_price_low_Dollar']   = elem_price_low
                data['elem_price_high_Dollar']  = elem_price_high
                data['elem_star']               = elem_star
                data['store_feedbackscore']     = store_feedbackscore
                data['store_sellerpositivefeedbackpercentage'] = store_sellerpositivefeedbackpercentage
                data['page_count']              = data['count']
                data['item_count']              = range(L_1)
                del data['count']
                del data['elem_price']

##                print data.head(5)
            except Exception as e:
                print target,' no data'
                data = pd.DataFrame({})
                print("open exception: %s: %s\n" %(e.message, e.args))

            if n == 0:
                df = data
            elif (category != Last_category):
                print 'save '+Last_category
                print len(df)
                writer = pd.ExcelWriter('data/' + Last_category+'.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                df = data
            elif n == L-1:
                df = df.append(data)
                writer = pd.ExcelWriter('data/' + Last_category+'.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1')
                writer.save()
            else:
                df = df.append(data)
                
        print 'finish'
