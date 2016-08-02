# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import numpy as np


class AliListPipeline(object):
    def __init__(self):
        self.df = pd.DataFrame({})
        self.count = 0

    def saveExcel(self,df,name):
        writer = pd.ExcelWriter(U'F:/GitHub/Hound_data/' + name+'.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def process_item(self, item, spider):
        self.count = self.count + 1
        # print item
        print self.count
        temp = pd.DataFrame({'cate_1':[item['cate_1']],\
                             'cate_2':[item['cate_2']],\
                             'cate_3':[item['cate_3']],\
                             'cate_4':[item['cate_4']],\
                             'cate_5':[item['cate_5']],\
                             'search_count':[item['search_count']],\
                             'item_url':[item['item_url']] \
                             })
        # print self.df
        self.df = self.df.append(temp)
        if self.count >= 2800:
            print 'save :',self.count
            self.saveExcel(self.df,'item_list')
            self.df.to_csv(U'F:/GitHub/Hound_data/item_list.csv')
        return item


class AliPipeline(object):
    def __init__(self):
        self.df = pd.DataFrame({})
        self.createVar = locals()

    def process_item(self, item, spider):
        print '#############################################'
        print item['end_flag']
        name = item['name']
        # print 'item len: ',len(item['df'])
        if item['end_flag'] == 0:
            try:
                self.createVar[name] = self.createVar[name].append(item['df'])
                print name
                print len(self.createVar[name])
            except Exception,e:
                print Exception,":",e
                try:
                    self.createVar[name] = item['df']
                    print 'new:'+name
                except Exception,e:
                    print '#######################################################################################################################################'
                    print 'item df error'
                    print type(item['df'])
                    print item['df']

        else :
            try:
                self.createVar[name] = self.createVar[name].append(item['df'])
                print name
                print len(self.createVar[name])
            except Exception,e:
                print Exception,":",e
                try:
                    self.createVar[name] = item['df']
                    print 'new:'+name
                except Exception,e:
                    print '#######################################################################################################################################'
                    print 'item df error'
                    self.createVar[name] = self.df_null
                    print type(item['df'])
                    # print item['df']

            try:
                # print self.createVar[name]
                self.createVar[name] = self.data_reduction(self.createVar[name])
                # self.createVar[name].to_csv('data/'+name+'.csv')
                self.createVar[name].to_csv(U'F:/GitHub/Hound_data/'+name+'.csv')
                self.saveExcel(self.createVar[name],name)
                del self.createVar[name]
            except Exception,e:
                print '#######################################################################################################################################'
                print 'EndFlag = 1'
                print 'Error Item: ',self.createVar[name]
                print 'Error message: ',Exception,":",e
        return item



    def saveExcel(self,df,name):
        # writer = pd.ExcelWriter('data/' + name+'.xlsx', engine='xlsxwriter')
        writer = pd.ExcelWriter(U'F:/GitHub/Hound_data/' + name+'.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def data_reduction(self,data):
        L_1 = len(data)
        print L_1

        elem_feedback        = data['elem_feedback'].values
        elem_order           = data['elem_order'].values
        elem_price           = data['elem_price'].values
        elem_price_low       = elem_price.copy()  # shallow copy ,(deepcopy() for deep copy)
        elem_price_high      = elem_price.copy()
        elem_original_price           = data['elem_original_price'].values
        elem_original_price_low       = elem_original_price.copy()  # shallow copy ,(deepcopy() for deep copy)
        elem_original_price_high      = elem_original_price.copy()
        elem_star            = data['elem_star'].values
        store_feedbackscore  = data['store_feedbackscore'].values
        store_sellerpositivefeedbackpercentage = data['store_sellerpositivefeedbackpercentage'].values

        for i in range(L_1):
            try:
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

                if elem_original_price[i]=='none':
                    elem_original_price_low[i] = np.nan
                    elem_original_price_high[i] = np.nan
                else:
                    elem_original_price[i] = elem_original_price[i].replace('US $','')
                    elem_original_price[i] = elem_original_price[i].replace(',','')
                    if elem_original_price[i].find(' - ') == -1:
                        elem_original_price_low[i]  = float(elem_original_price[i])
                        elem_original_price_high[i] = float(elem_original_price[i])
                    else:
                        elem_original_price_temp = elem_original_price[i].split(' - ')
                        elem_original_price_low[i]  = float(elem_original_price_temp[0])
                        elem_original_price_high[i] = float(elem_original_price_temp[1])

                if elem_star[i]=='none':
                    elem_star[i] = np.nan
                else:
                    elem_star[i] = elem_star[i].replace('Star Rating: ','')
                    elem_star[i] = float(elem_star[i].replace(' out of 5',''))

                if store_feedbackscore[i]=='none' or store_feedbackscore[i]=='nan':
                    store_feedbackscore[i] = np.nan
                else:
                    store_feedbackscore[i] = store_feedbackscore[i].replace(',','')
                    store_feedbackscore[i] = int(store_feedbackscore[i])

                if store_sellerpositivefeedbackpercentage[i]=='none' or store_sellerpositivefeedbackpercentage[i]=='':
                    store_sellerpositivefeedbackpercentage[i] = np.nan
                else:
                    store_sellerpositivefeedbackpercentage[i] = float(store_sellerpositivefeedbackpercentage[i])
            except Exception,e:
                print Exception,":",e
                print 'elem_feedback: ',elem_feedback[i]
                print 'elem_order: ',elem_order[i]
                print 'elem_price: ',elem_price[i]
                print 'elem_original_price: ',elem_original_price[i]
                print 'elem_star: ',elem_star[i]
                print 'store_feedbackscore: ',store_feedbackscore[i]
                print 'store_sellerpositivefeedbackpercentage: ',store_sellerpositivefeedbackpercentage[i]

        data['elem_feedback']           = elem_feedback
        data['elem_order']              = elem_order
        data['elem_price_low_Dollar']   = elem_price_low
        data['elem_price_high_Dollar']  = elem_price_high
        data['elem_original_price_low_Dollar']   = elem_original_price_low
        data['elem_original_price_high_Dollar']  = elem_original_price_high
        data['sell_off_LvsL']           = data['elem_price_low_Dollar']/data['elem_original_price_low_Dollar']
        data['sell_off_HvsH']          = data['elem_price_high_Dollar']/data['elem_original_price_high_Dollar']
        data['elem_star']               = elem_star
        data['store_feedbackscore']     = store_feedbackscore
        data['store_sellerpositivefeedbackpercentage'] = store_sellerpositivefeedbackpercentage
        del data['elem_price']
        del data['elem_original_price']
        return data
