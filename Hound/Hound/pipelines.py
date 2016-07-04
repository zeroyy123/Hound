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
        writer = pd.ExcelWriter('data/' + name+'.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def process_item(self, item, spider):
        self.count = self.count + 1
        print self.count
        temp = pd.DataFrame({'catepory':[item['catepory']],\
                             'son_catepory':[item['son_catepory']],\
                             'gra_son_cate':[item['gra_son_cate']],\
                             'search_count':[item['search_count']],\
                             'item_url':[item['item_url']] \
                             })
        self.df = self.df.append(temp)
        if self.count == 1700:
            print self.df
            self.saveExcel(self.df,'item_list')
            self.df.to_csv('data/item_list.csv')
            print self.df
        return item


class AliPipeline(object):
    def __init__(self):
        self.df = pd.DataFrame({})
        self.createVar = locals()

    def process_item(self, item, spider):
        print '#############################################'
        print item['end_flag']
        name = item['category'].replace(' ','')
        name = name.replace("'",'')
        name = name.replace('&','')

        if item['end_flag'] == 0:
            try:
                self.createVar[name] = self.createVar[name].append(item['df'])
                print name
                print len(self.createVar[name])
            except Exception,e:
                print Exception,":",e
                self.createVar[name] = item['df']
                print 'new:'+name
        else :
            print self.createVar[name]
            self.createVar[name].to_csv('data/'+item['category']+'.csv')
            self.saveExcel(self.createVar[name],name)
        return item



    def saveExcel(self,df,name):
        writer = pd.ExcelWriter('data/' + name+'.xlsx', engine='xlsxwriter')
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
        del data['elem_price']
        return data
