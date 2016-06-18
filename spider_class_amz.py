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