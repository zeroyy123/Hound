# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import threading

class spider_aliexp():
    def __init__(self):
        self.driver = []
        self.mutex = threading.Lock()
        self.results = pd.DataFrame({})
        self.results_title = []
        self.results_price = []
        self.results_commit_score = []
        self.results_commit_times = []
        self.results_orders = []
        self.results_store = []


    def open_web(self,proxy_ip,url):
        PROXY = proxy_ip # IP:PORT or HOST:PORT
        if url == '':
            url = "http://www.aliexpress.com"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir="+ os.path.abspath(r"C:\Users\yy\AppData\Local\Google\Chrome\User Data"))
        if PROXY != '':
            chrome_options.add_argument('--proxy-server=http://'+PROXY)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
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

    def get_results_count(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="search-result"]/p/strong[@class="search-count"]')
        print elems[0].text

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

    def get_page_num(self):

        elems = self.driver.find_elements_by_xpath('//span[@id="pagination-max"]')
        page_num = elems[0].get_attribute('innerHTML')
        print 'page_max:'+page_num
        return page_num

    def go_page(self,page):
        elems = self.driver.find_elements_by_xpath('//input[@id="pagination-bottom-input"]')
        elems[0].send_keys(Keys.BACKSPACE + Keys.BACKSPACE + Keys.BACKSPACE + str(page) + Keys.RETURN)
        time.sleep(1)
        js="var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)

    def get_item(self):

        page_type = self.driver.find_elements_by_xpath('//div[@id="main-wrap"]')[0].get_attribute('class')
        # print page_type
        if page_type == 'main-wrap gallery-mode':
            print page_type
            xpath_root = '//div[@id="list-items"]/ul/li'
            xpath_title = '//div[@class="info"]/h3/a'
            xpath_price = '//div[@class="info"]/span[@class="price price-m"]/span[1]'
            xpath_commit_score = '//div[@class="info"]/div[@class="rate-history"]/span[@class="star star-s"]'
            xpath_commit_times = '//div[@class="info"]/div[@class="rate-history"]/a[@class="rate-num "]'
            xpath_orders = '//div[@class="info"]/div[@class="rate-history"]/span[@class="order-num"]/a/em'
            xpath_store  = '//div[@class="info-more"]/div[@class="store-name-chat"]/div/a'
        elif page_type == 'main-wrap ':
            print page_type
            xpath_root = '//div[@id="main-wrap"]/ul[@id="list-items"]/li'
            xpath_title = '//div[@class="detail"]/h3/a'
            xpath_price = '//div[@class="info infoprice"]/span[@class="price price-m"]/span[1]'
            xpath_commit_score = '//div[@class="info infoprice"]/div[@class="rate-history"]/span[@class="star star-s"]'
            xpath_commit_times = '//div[@class="info infoprice"]/div[@class="rate-history"]/a'
            xpath_orders       = '//div[@class="info infoprice"]/div[@class="rate-history"]//em[@title="Total Orders"]'
            xpath_store        = '//div[@class="detail"]/div/span/a[2]'
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

        thrs = []
        t = threading.Thread(target = self.get_sub_item, args = ('title',num,xpath_root,xpath_title,''))
        thrs.append(t)
        t = threading.Thread(target = self.get_sub_item, args = ('price',num,xpath_root,xpath_price,'',))
        thrs.append(t)
        t = threading.Thread(target = self.get_sub_item, args = ('commit_score',num,xpath_root,xpath_commit_score,'title'))
        thrs.append(t)
        t = threading.Thread(target = self.get_sub_item, args = ('commit_times',num,xpath_root,xpath_commit_times,''))
        thrs.append(t)
        t = threading.Thread(target = self.get_sub_item, args = ('orders',num,xpath_root,xpath_orders,''))
        thrs.append(t)
        t = threading.Thread(target = self.get_sub_item, args = ('store',num,xpath_root,xpath_store,'title'))
        thrs.append(t)

        for t in thrs:
            t.setDaemon(True) #保护进程不要在主进程结束后 也被结束
            t.start()
        for t in thrs:
            t.join()

        # elem_title = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_title,attribute='')
        # elem_price = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_price,attribute='')
        # elem_commit_score = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_commit_score,attribute='title')
        # elem_commit_times = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_commit_times,attribute='')
        # elem_orders = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_orders,attribute='')
        # elem_store = self.get_sub_item(num=num,xpath_root=xpath_root,xpath_item=xpath_store,attribute='title')

        if num > 1:
            self.results = self.results.append(pd.DataFrame({'elem_title':self.results_title,\
                                                                 'elem_price':self.results_price,\
                                                                 'elem_commit_score':self.results_commit_score,\
                                                                 'elem_commit_times':self.results_commit_times,\
                                                                 'elem_orders': self.results_orders,\
                                                                 'elem_store':self.results_store}))
        else:
            self.results = self.results.append(pd.DataFrame({'elem_title':[self.results_title],\
                                                                 'elem_price':[self.results_price],\
                                                                 'elem_commit_score':[self.results_commit_score],\
                                                                 'elem_commit_times':[self.results_commit_times],\
                                                                 'elem_orders': [self.results_orders],\
                                                                 'elem_store':[self.results_store]}))

        # for i in range(num):
        #     elem_title = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_title)
        #     elem_title = elem_title[0].text
        #     elem_price = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_price)
        #     elem_commit_score = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_commit_score)
        #     elem_commit_times = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_commit_times)
        #     elem_orders = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_orders)
        #     elem_store  = self.driver.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_store)
        #     try:
        #         elem_price = elem_price[0].text
        #     except:
        #         elem_price = 'none'
        #     try:
        #         elem_commit_score = elem_commit_score[0].get_attribute("title")
        #     except:
        #         elem_commit_score = 'none'
        #     try:
        #         elem_commit_times = elem_commit_times[0].text
        #     except:
        #         elem_commit_times = 'none'
        #     try:
        #         elem_orders = elem_orders[0].text
        #     except:
        #         elem_orders = 'none'
        #     try:
        #         elem_store = elem_store[0].get_attribute("title")
        #     except:
        #         elem_store = 'none'
        #
        #     self.results = self.results.append(pd.DataFrame({'elem_title':[elem_title],\
        #                                                      'elem_price':[elem_price],\
        #                                                      'elem_commit_score':[elem_commit_score],\
        #                                                      'elem_commit_times':[elem_commit_times],\
        #                                                      'elem_orders':[elem_orders],\
        #                                                      'elem_store':[elem_store]}))

    def get_sub_item(self,item_name,num,xpath_root,xpath_item,attribute):
        results = []
        if self.mutex.acquire(1):
            driver_temp = self.driver
            self.mutex.release()
        for i in range(num):
            elems = driver_temp.find_elements_by_xpath(xpath_root+'['+str(i+1)+']'+xpath_item)
            try:
                if attribute == '':
                    elem = elems[0].text
                else:
                    elem = elems[0].get_attribute(attribute)
            except:
                elem = 'none'
            results.append(elem)

            if item_name == 'title':
                self.results_title = results
            elif item_name == 'price':
                self.results_price = results
            elif item_name == 'commit_score':
                self.results_commit_score = results
            elif item_name == 'commit_times':
                self.results_commit_times = results
            elif item_name == 'orders':
                self.results_orders = results
            elif item_name == 'store':
                self.results_store = results
        # return results

    def next_page(self):
        elems = self.driver.find_elements_by_xpath('//div[@class="ui-pagination-navi util-left"]/a[@class = "page-next ui-pagination-next"]')
        elems[0].click()
        time.sleep(1)

        js="var q=document.body.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1)
        js="var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)

    def driver_quit(self):
        self.driver.quit()

    def open_mode_sel(self,target,proxy_ip,url):
        if url == '':
            self.open_web(proxy_ip)
            self.search_item(target)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(1)
        else:
            self.open_web(proxy_ip,url)
            js="var q=document.body.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(1)

    def save_xlsx(self,target):
        writer = pd.ExcelWriter(target+'.xlsx', engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        self.results.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def process(self,target,proxy_ip,target_num,url):
        self.open_mode_sel(target,proxy_ip,url)
        self.get_results_count()
        page_num = self.get_page_num()
        if target_num > page_num:
            target_num = page_num

        for i in range(target_num):
            print i
            self.get_item()
            # self.next_page()
            [a,b] = divmod(i,10)
            if a != 0 and b == 0:
                self.save_xlsx(target)
                self.driver_quit()
                self.open_mode_sel(target,proxy_ip,url)
                print 'backup:',i
            self.go_page(i+2)
        self.driver_quit()
        self.results.to_csv(target+'.csv',encoding='utf-8')
        self.save_xlsx(target)

        print self.results
        print 'results number :',len(self.results)
        print page_num
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









