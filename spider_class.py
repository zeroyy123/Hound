# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

class spider_aliexp():
    def __init__(self):
        self.driver = []
        self.results = pd.DataFrame({})

    def open_web(self,proxy_ip,webdrv,url):
        self.open_web_driver(proxy_ip,webdrv)
        self.open_web_url(url)

    def open_web_driver(self,proxy_ip,webdrv):
        PROXY = proxy_ip # IP:PORT or HOST:PORT
        
        if webdrv == 'PhantomJS':
            service_args = [
                                '--proxy='+proxy_ip ,
                                '--proxy-type=http',
                            ]
            self.driver = webdriver.PhantomJS(service_args=service_args)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\yy\AppData\Local\Google\Chrome\User Data"))
            if PROXY != '':
                chrome_options.add_argument('--proxy-server=http://'+PROXY)
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        



        
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
#        js="var q=document.body.scrollTop=10000"
#        self.driver.execute_script(js)

    def get_search_count(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="search-result"]//strong[@class="search-count"]')
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

    def go_page(self,page):
        elems = self.driver.find_elements_by_xpath('//input[@id="pagination-bottom-input"]')
        elems[0].send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + str(page))
        elems[0].send_keys(Keys.RETURN)
        
        time.sleep(0.5)
        js="var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)

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
        
    def next_page(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="ui-pagination-navi util-left"]/a[@class = "page-next ui-pagination-next"]')
        elems[0].click()
        time.sleep(0.5)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(0.5)
##        js="var q=document.body.scrollTop=10000"
##        self.driver.execute_script(js)

    def driver_quit(self):
        self.driver.quit()

    def open_mode_sel(self,target,proxy_ip,webdrv,url):
        if url == '':
            self.open_web(proxy_ip,webdrv)
            self.search_item(target)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(0.5)
        else:
            self.open_web(proxy_ip,webdrv,url)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(0.5)

    def save_xlsx(self,target):
        writer = pd.ExcelWriter('data/' + target+'.xlsx', engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        self.results.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def process(self,target,proxy_ip,webdrv,target_num,url):
        self.open_mode_sel(target,proxy_ip,webdrv,url)
        search_count = self.get_search_count()
        
        print 'search_count:',search_count
        
        page_num = self.get_page_num()

        print 'page_max:',page_num
        
        if target_num > page_num:
            target_num = page_num

        print target_num
        
        for i in range(target_num):
            print target,': ',i
            state = self.get_item()
            if state == 'no items':
                break
            elif state == 'error':
                break
            
##            [a,b] = divmod(i,10)
##            if a != 0 and b == 0:
##                self.save_xlsx(target)
##                self.driver_quit()    ## for phantomjs test, if use chrome, driver must quit every 10 page
##                self.open_mode_sel(target,proxy_ip,url)
##                print 'backup:',i
            
            if len(self.results) >= search_count:
                break
            if i < (target_num - 1):
                self.next_page()            
##                self.go_page(i+2)  ## phantomjd cann't use send key
        
        self.driver_quit()
        self.results.to_csv('data/'+target+'.csv',encoding='utf-8')
        self.save_xlsx(target)

##        print self.results
        print 'results number :',len(self.results)
        print 'finish'

class spider_amz():
##chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
##os.environ["webdriver.chrome.driver"] = chromedriver
##
    def __init__(self):
        self.driver = []
        self.results = pd.DataFrame({})

    def open_web(self,proxy_ip):
        PROXY = proxy_ip # IP:PORT or HOST:PORT
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\yy\AppData\Local\Google\Chrome\User Data"))
        if PROXY != '':
            chrome_options.add_argument('--proxy-server=http://'+PROXY)
##        chrome_options.add_argument('--proxy-server=124.232.165.99:80')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get("http://www.amazon.com/")

    def search_item(self,target):
        search_key = target
        elems = self.driver.find_elements_by_xpath('//input[@id = "twotabsearchtextbox"]')
        ##print len(elems)
        elems[0].send_keys(search_key + Keys.RETURN)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1)
##        js="var q=document.body.scrollTop=10000"
##        self.driver.execute_script(js)

    def get_page_num(self):
        elems = self.driver.find_elements_by_xpath('//div[@id="centerBelowMinus"]//span[@class = "pagnDisabled"]')
        page_num = elems[0].text
        return page_num


    def get_item(self):
        xpath_root = '//ul[@id = "s-results-list-atf"]/li'
        xpath_title = '//div[@class="a-row a-spacing-none"]/a/h2'
        xpath_price = '//div[@class="a-row a-spacing-none"]/a/span'
        xpath_commit_score = '/div/div[@class="a-row a-spacing-none"]//a[@class = "a-popover-trigger a-declarative"]/i/span[@class="a-icon-alt"]'
        xpath_commit_times = '/div/div[@class="a-row a-spacing-none"]/a'

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
        return_data = []
        for i in range(num):
            elem_title = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_title)
            elem_title = elem_title[0].text
            elem_price = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_price)
            elem_commit_score = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_commit_score)
            elem_commit_times = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_commit_times)

            try:
                elem_price = elem_price[0].text
            except:
                elem_price = 'none'
            try:
                ## Get text from hidden elements
                elem_commit_score = elem_commit_score[0].get_attribute('innerHTML')
            except:
                elem_commit_score = 'none'
            try:
                elem_commit_times = elem_commit_times[0].text
            except:
                elem_commit_times = 'none'

            self.results = self.results.append(pd.DataFrame({'elem_title':[elem_title],\
                                                             'elem_price':[elem_price],\
                                                             'elem_commit_score':[elem_commit_score],\
                                                             'elem_commit_times':[elem_commit_times]}))


    def next_page(self):
        elems = self.driver.find_elements_by_xpath('//div[@id="centerBelowMinus"]//span[@id = "pagnNextString"]')
        elems[0].click()
        time.sleep(1)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1)
        js="var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)

    def driver_quit(self):
        self.driver.quit()

    def process(self,target,proxy_ip,target_num):
        self.open_web(proxy_ip)

##        target = 'hp laptop'
        self.search_item(target)

        page_num = self.get_page_num()
        if target_num > page_num:
            target_num = page_num

        for i in range(target_num):
            print i
            self.get_item()
            self.next_page()









