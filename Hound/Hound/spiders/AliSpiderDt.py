from bs4 import BeautifulSoup
import pandas as pd
import re
from getItemSub1 import *
from getItemSub2 import *

class AliSpiderDt():
    def __init__(self,response,StartFlag):
        self.response = response
        if StartFlag == 1:
            print 'StartFlag == 1'

        try:
            self.soup= BeautifulSoup(response.body, "html.parser")
        except Exception,e:
            print '#######################################################################################################################################'
            print 'soup read error: ',name
            print Exception,":",e

        self.df_null = pd.DataFrame({'count':[],\
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

    def get_next_page(self):
        try:
            elems = self.soup.find_all('a',class_='page-next ui-pagination-next')
            next_url = 'http:'+elems[0].get('href')
            print 'next url:'
            return next_url
        except:
            print 'next url:'
            return 'none'

        return results

    def get_item(self):
        try:
            elems = self.soup.find_all('div',id='main-wrap')
            page_type = elems[0].get('class')
        except Exception,e:
            print 'get item page type error'
            print Exception,":",e
        if page_type[1] == 'gallery-mode': #'main-wrap gallery-mode'
            obj = getItemSub1(self.soup)
            return obj.get_item()
        elif page_type[1] == '': #'main-wrap '
            obj = getItemSub2(self.soup)
            return obj.get_item()
        else:
            print self.df_null
            return self.df_null