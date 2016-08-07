from bs4 import BeautifulSoup
import pandas as pd
import re

class getItemSub2():
    def __init__(self, soup):
        self.soup = soup
        self.df_null = pd.DataFrame({'count':[], \
                                    'elem_ID':[], \
                                     'elem_title':[], \
                                     'elem_price':[], \
                                     'elem_original_price':[], \
                                     'elem_order':[], \
                                     'elem_feedback':[], \
                                     'elem_star':[], \
                                     'elem_store':[], \
                                     'store_feedbackscore':[], \
                                     'store_sellerpositivefeedbackpercentage':[], \
                                     'elem_ship':[]
                                    })

    def get_list(self):
        elems = self.soup.find_all('ul', id='list-items')
        if len(elems) == 0:
            return 'null'
        elems = elems[0].find_all('li')
        if len(elems) == 0:
            return 'null'

        print 'li: ', len(elems)
        return elems
    
    def get_detial(self, elem):
        try:
            elem_detail = elem.find_all('div', class_='detail')
            elem_detail = elem_detail[0]
            return elem_detail
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_detail error'
            return 'error'
    
    def get_info(self, elem):
        try:
            elem_info = elem.find_all('div', class_='info infoprice')
            elem_info = elem_info[0]
            return elem_info
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_info error'
            return 'error'
    
    def get_id(self, elem):
        try:
            elem_ID = elem.get('qrdata')
            return elem_ID
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_ID error'
            return 'none'
    
    def get_title(self, elem):
        try:
            elem_title = elem.find_all('h3')
            elem_title = elem_title[0].find_all('a')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_title error'
            return 'none'
        
        elem_title = elem_title[0].text
        return elem_title
    
    def get_price(self, elem):
        try:
            elem_price    = elem.find_all('span', class_='value')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_price error'
            return 'none'
        
        try:
            elem_price = elem_price[0].text
        except:
            elem_price = 'none'
        return elem_price

    def get_org_price(self, elem):
        try:
            elem_original_price = elem.find_all('del', class_='original-price')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_original_price error'
            return 'none'
        
        try:
            elem_original_price = elem_original_price[0].text
        except:
            elem_original_price = 'none'
        return elem_original_price
    
    def get_order(self, elem):
        try:
            elem_order    = elem.find_all('em', title='Total Orders')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_order error'
            return 'none'
        
        try:
            elem_order = elem_order[0].text
        except:
            elem_order = 'none'
        return elem_order
    
    def get_star(self, elem):
        try:
            elem_star     = elem.find_all('span', class_='star star-s')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_star error'
            return 'none'
        try:
            elem_star = elem_star[0].get('title')
        except:
            elem_star = 'none'
        return elem_star

    def get_feedback(self, elem):
        try:
            elem_feedback = elem.find_all('a', class_='rate-num ')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_feedback error'
            return 'none'
        try:
            elem_feedback = elem_feedback[0].text
        except:
            elem_feedback = '(0)'
        return elem_feedback
    
    def get_store(self, elem):
        try:
            elem_store    = elem.find_all(name='a',  attrs={'class':re.compile(r"(store|store j-p4plog)")})
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_store error'
            return 'none'
        try:
            elem_store = elem_store[0].get('title')
        except:
            elem_store = 'none'
        return elem_store

    def get_store_property(self,elem):
        try:
            store_property = elem.find_all('img', class_='score-icon')
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get store_property error'
            return ['none', 'none']
        try:
            store_feedbackscore = store_property[0].get('feedbackscore')
            store_sellerpositivefeedbackpercentage = store_property[0].get('sellerpositivefeedbackpercentage')
        except:
            store_feedbackscore = 'none'
            store_sellerpositivefeedbackpercentage = 'none'
        return [store_feedbackscore,store_sellerpositivefeedbackpercentage]

    def get_shipping(self,elem):
        try:
            elem_ship = elem.find_all('strong')
            # print elem_ship
            if len(elem_ship) != 0:
                elem_ship = elem_ship[0].text
            else:
                elem_ship = elem.find_all('dd', class_='price')
                if len(elem_ship) != 0:
                    elem_ship = elem_ship[0].text
                else:
                    elem_ship = 'none'
            return elem_ship
        except Exception, e:
            print '#######################################################################################################################################'
            print Exception, ":", e
            print 'get elem_ship error'
            return 'none'

    def get_item(self):
        print 'get item mode 2'
        results = pd.DataFrame({})

        Lists = self.get_list()
        if Lists == 'null':
            return self.df_null

        for i in range(len(Lists)):
            elem_ID             = self.get_id(Lists[i])        
            elem_detail         = self.get_detial(Lists[i])    
            elem_info           = self.get_info(Lists[i])
            elem_order          = self.get_order(Lists[i])
            
            elem_title          = self.get_title(elem_detail)
            elem_price          = self.get_price(elem_info)
            elem_original_price = self.get_org_price(elem_info)
            elem_star           = self.get_star(elem_info)
            elem_feedback       = self.get_feedback(elem_info)
            elem_ship           = self.get_shipping(elem_info)

            elem_store          = self.get_store(elem_detail)
            [store_feedbackscore,store_sellerpositivefeedbackpercentage] = self.get_store_property(elem_detail)


            results = results.append(pd.DataFrame({'count':[i], \
                                                            'elem_ID':[elem_ID], \
                                                             'elem_title':[elem_title], \
                                                             'elem_price':[elem_price], \
                                                             'elem_original_price':[elem_original_price], \
                                                             'elem_order':[elem_order], \
                                                             'elem_feedback':[elem_feedback], \
                                                             'elem_star':[elem_star], \
                                                             'elem_store':[elem_store], \
                                                             'store_feedbackscore':[store_feedbackscore], \
                                                             'store_sellerpositivefeedbackpercentage':[store_sellerpositivefeedbackpercentage], \
                                                            'elem_ship':[elem_ship]\
                                                            }))
        return results