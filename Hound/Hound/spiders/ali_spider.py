import scrapy
from items import HoundItem
from bs4 import BeautifulSoup
import pandas as pd
import re
from AliSpiderDt import *
import numpy as np


class AliSpider(scrapy.Spider):
    name = "ali"
    allowed_domains = ["aliexpress.com"]

    df_null = pd.DataFrame({'count':[],\
                                    'elem_ID':[],\
                                     'elem_title':[],\
                                     'elem_price':[],\
                                     'elem_original_price':[],\
                                     'elem_order':[],\
                                     'elem_feedback':[],\
                                     'elem_star':[],\
                                     'elem_store':[],\
                                     'store_feedbackscore':[],\
                                     'store_sellerpositivefeedbackpercentage':[],\
                                     'elem_ship':[]
                                    })

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

    index_df = pd.read_csv(U'F:/GitHub/Hound_data/item_list.csv')
    print len(index_df)

    def __init__(self, start=0,end=0, *args, **kwargs):
        super(AliSpider, self).__init__(*args, **kwargs)
        print int(start)
        print int(end)

        self.start_urls = []
        urls = ((pd.read_csv(U'F:/GitHub/Hound_data/item_list.csv'))['item_url'].values)[int(start):int(end)]
        count = 0
        for url in urls:
            print count
            count = count + 1
            [name,cate_1,cate_2,cate_3,cate_4,cate_5] = self.gen_name(url)
            try:
                df = pd.read_csv(U'F:/GitHub/Hound_data/'+name+'.csv')
            except:
                print '#######################miss:',name
                print url
                self.start_urls.append(url)

        # self.start_urls = (pd.read_csv(U'F:/GitHub/Hound_data/item_list.csv'))['item_url'].values[int(start):int(end)]  #8:31start
        print 'urls length:',len(self.start_urls)



    def parse(self, response,StartFlag = 1,name='',cate_1='1',cate_2='1',cate_3='1',cate_4='1',cate_5='1'):
        print '#########'
        print response.url
        if StartFlag == 1:
            print 'StartFlag == 1'
            [name,cate_1,cate_2,cate_3,cate_4,cate_5] = self.gen_name(response.url)

        AS = AliSpiderDt(response,StartFlag)

        df = AS.get_item()
        next_url = AS.get_next_page()
        print   next_url


        item = HoundItem()
        if next_url == 'none':
            item['end_flag'] = 1
        else:
            item['end_flag'] = 0

        try:
            item['name'] = name   ### no data rerurn in the cwarl end ,need to debug
            df['cate_1'] = cate_1
            df['cate_2'] = cate_2
            df['cate_3'] = cate_3
            df['cate_4'] = cate_4
            df['cate_5'] = cate_5

            item['df'] = df
        except Exception,e:
            print Exception,":",e
        yield item
        yield scrapy.Request(next_url,headers=self.headers,callback=lambda response,StartFlag=0,\
                                name=name,cate_1=cate_1,cate_2=cate_2,cate_3=cate_3,cate_4=cate_4,cate_5=cate_5 \
                                :self.parse(response,StartFlag,name,cate_1,cate_2,cate_3,cate_4,cate_5))


    def gen_name(self,url):
        name = self.index_df[self.index_df['item_url'] == url]
        name = name.fillna('')
        cate_1 = (name['cate_1'].values)[0]
        cate_2 = (name['cate_2'].values)[0]
        cate_3 = (name['cate_3'].values)[0]
        cate_4 = (name['cate_4'].values)[0]
        cate_5 = (name['cate_5'].values)[0]

        name = (name['cate_1'].values)[0] + '_' + (name['cate_2'].values)[0] + '_' + (name['cate_3'].values)[0] + '_' + (name['cate_4'].values)[0] + '_' + (name['cate_5'].values)[0]
        name = name.replace(' ','')
        name = name.replace("'",'')
        name = name.replace('&','')
        name = name.replace('/','_')
        name = name.replace('"','')
        name = name.replace('*','x')
        name = name.replace('<','')
        name = name.replace('>','')
        return [name,cate_1,cate_2,cate_3,cate_4,cate_5]
