# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import threading
import time
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from selenium import webdriver

class agent:
    def __init__(self):

        self.User_Agent      = 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                                        AppleWebKit/537.36 (KHTML, like Gecko) \
                                        Chrome/47.0.2526.80 Safari/537.36 \
                                        QQBrowser/9.3.6874.400 \
                                        Query String Parameters \
                                        view source      \
                                        view URL encoded \
                                        '

        self.headers = { 'User-Agent' : self.User_Agent}
        self.results = []
        self.mutex = threading.Lock()
        
    def get_proxy(self,num):
        ##for page in range(1, 160):
        results = []
        for n in range(num):
            # url = 'http://www.xicidaili.com/nt/' + str(n+1)
            url = 'http://www.xicidaili.com/nn/' + str(n+1)
            # url = 'http://www.xicidaili.com/wn/' + str(n+1)
            request = urllib2.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')

            tempPage = BeautifulSoup(pageCode,"lxml")
            tempPage = tempPage.find_all('div',id="wrapper")
            tempPage = tempPage[0].find_all('table',id="ip_list")
            ##print tempPage[0].prettify()
            tempPage = tempPage[0].find_all('tr')

            for i in range(len(tempPage)):
                if i >0 :
                    item = tempPage[i].find_all('td')
                    results.append([item[1].text,item[2].text,item[5].text])

        print 'ip_addr_num:', len(results)
        return results


    def verify_proxy(self,target,ip_addrs,mark,fail_time):
        if target == 'ali':
            # url = 'https://www.aliexpress.com'
            url = 'http://www.aliexpress.com/category/5090301/mobile-phones.html?pvId=200001044-200658763'
            fail_words = '400 Bad Request'
        elif target == 'amz':
            url = 'https://www.amazon.com/'
            fail_words = 'Robot Check'
        elif target == 'jd':
            url = 'https://www.jd.com/'
            fail_words = ' '
        elif target == 'tb':
            url = 'https://www.taobao.com/'
            fail_words = ' '
        else:
            url = 'https://www.google.com'
            fail_words = ' '

        if mark == 1:
            print 'target url:',url

        # urllib2 mode
        # request = urllib2.Request(url,headers = self.headers)

        fail_count = 0
        for i in range(len(ip_addrs)):
            ip_addr = ip_addrs[i]
            temp = ip_addr[0]+':'+ip_addr[1]
            print mark,': ',i,' ',temp

            # urllib2 mode
            # request.set_proxy(ip_addr[0]+':'+ip_addr[1],'http')
            service_args = [
                                '--proxy='+temp,
                                '--proxy-type=http',
                                '--load-images=no',
                                '--disk-cache=yes',
                            ]
            try:
                driver = webdriver.PhantomJS(service_args=service_args,desired_capabilities={'phantomjs.page.settings.resourceTimeout': '1000'})
                driver.set_page_load_timeout(10)
                start_time = datetime.datetime.now()
                driver.get(url)
                response = driver.page_source

                # urllib2 mode
                # response = urllib2.urlopen(request,timeout=fail_time)

                end_time = datetime.datetime.now()
                total_ms = (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds/1000

                tempPage = BeautifulSoup(response, "html.parser")
                # tempPage = BeautifulSoup(pageCode,"lxml")
                tempPage = tempPage.find_all('title')

                if tempPage[0].text == 'Mobile Phones Directory of Mobile Phones, Phones &amp; Telecommunications and more on Aliexpress.com':
                    acq_flag = 1
                else:
                    acq_flag = 0

                # print 'thread :',mark
                # print temp + ' speed: ' + str(total_ms)
                # print tempPage[0].text
            except:
                acq_flag = 0
                fail_count = fail_count + 1
            try:
                driver.quit()
            except:
                print 'Thread ',mark,'driver quit unsuccess'

            if acq_flag == 1:
                if self.mutex.acquire(1):
                        self.results.append([temp,total_ms])
                        self.mutex.release()
                else:
                    print 'Thread ',mark,'lock request fail'

                print temp + ' speed: ' + str(total_ms)
                print tempPage[0].text
                print 'Thread ',mark,'acquired'

                # urllib2 mode
                # print 'check again'
                # try:
                #     start_time = datetime.datetime.now()
                #     pageCode = urllib2.urlopen(request,timeout=fail_time)
                #     end_time = datetime.datetime.now()
                #
                #     total_ms = total_ms + (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds/1000
                #     total_ms = total_ms/2
                #
                #     tempPage = BeautifulSoup(pageCode,"lxml")
                #     tempPage = tempPage.find_all('title')
                #
                #     if self.mutex.acquire(1):
                #         self.results.append([temp,total_ms])
                #         self.mutex.release()
                #     else:
                #         print 'Thread ',mark,'lock request fail'
                #
                #     print temp + ' speed: ' + str(total_ms)
                #     print tempPage[0].text
                #     print 'Thread ',mark,'acquired'
                # except:
                #     print 'fail'

        print mark,' proxy fail ',fail_count


    def mult_verify(self,target,page_num,fail_time):
        thrs = []
        results = self.get_proxy(page_num)
        
        for i in range(page_num):
            t = threading.Thread(target = self.verify_proxy, args = (target,results[i*100:(i+1)*100],i+1,fail_time,))
            thrs.append(t)
        for t in thrs:
            t.setDaemon(True) #保护进程不要在主进程结束后 也被结束
            t.start()
        for t in thrs:
            t.join()

        df = pd.DataFrame({})
        
        if len(self.results) > 0:
            for i in range(len(self.results)):
                df = df.append(pd.DataFrame({'ip_addr':[self.results[i][0]],'delay_ms':[self.results[i][1]]}))
            df = df.sort_values(by = 'delay_ms')
            print df
            df.to_csv(target+'_proxy_ip.csv')
            
##        print self.results
        print 'total results:',len(self.results)
        print 'finish'
        


##Ag = agent()
##Ag.mult_verify(2)

##results = Ag.get_proxy(1)
##for i in range(len(results)):
##    Ag.verify_proxy(results[i])
##
##print 'finish'



