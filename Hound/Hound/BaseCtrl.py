# -*- coding:utf-8 -*-
import pandas as pd
import MysqlDriver as MD
import numpy as np
import settings

class BaseCtrl():
    def __init__(self):
        self.list_path  = U'F:/GitHub/Hound_data/'

    def symbol_prune(self,symbol):
        symbol = symbol.replace(' ','')
        symbol = symbol.replace("'",'')
        symbol = symbol.replace('&','')
        symbol = symbol.replace('/','_')
        symbol = symbol.replace('"','')
        symbol = symbol.replace('*','x')
        symbol = symbol.replace('<','')
        symbol = symbol.replace('>','')
        return symbol

    def set_pipelines(self,target):
        if target == 'ali_list_spider':
            settings.ITEM_PIPELINES = {
             'Hound.pipelines.AliListPipeline': 300
            }
        elif target == 'ali_spider':
            settings.ITEM_PIPELINES = {
            'Hound.pipelines.AliPipeline': 300
            }

    def saveExcel(self,df,name):
        writer = pd.ExcelWriter(U'F:/GitHub/Hound_data/' + name+'.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def list_duplicate_delete(self,list_name = 'item_list'):
        cate_scan_len = 10
        list_path = self.list_path + list_name + '.csv'
        df = pd.read_csv(list_path)
        df['duplicate_mark'] = 0
        for i in range(len(df)):
            if i < len(df)-1:
                for j in range(i+1,len(df),1):
                    if df['item_url'].values[j] == df['item_url'].values[i]:
                        df['duplicate_mark'].values[j] = 1
                        print 'url duplicate: ',j
                        print 'data:',df.values[j]
        for i in range(len(df)-1,0,-1):
            if df['duplicate_mark'].values[i] == 1:
                df = df.drop(i)

        df['cates'] = ''
        for i in range(len(df)):
            temp_cates = ''
            for j in range(1,cate_scan_len,1):
                temp_name = 'cate_'+str(j)
                try:
                    a = df[temp_name].values[i]
                    temp_cates = temp_cates+df[temp_name].values[i]
                except:
                    break
            df['cates'].values[i] = temp_cates
        print df['cates'].values[0]

        for i in range(len(df)):
            if i < len(df)-1 and df['duplicate_mark'].values[i] != 1:
                count_dul = 0
                for j in range(i+1,len(df),1):
                    if df['cates'].values[j] == df['cates'].values[i]:
                        count_dul = count_dul + 1
                        df['duplicate_mark'].values[j] = 1
                        for k in range(1,cate_scan_len,1):
                            temp_name = 'cate_'+str(k)
                            try:
                                if df[temp_name].values[j] == np.nan:
                                    df[temp_name].values[j] = 'duplicates_'+str(count_dul)
                                    break
                            except:
                                print 'k: ',k
                                temp_name = 'cate_'+str(k-1)
                                df[temp_name].values[j] = df[temp_name].values[j] + '_duplicates_'+str(count_dul)
                                break
                        print ''
                        print 'cates duplicate: ',i,j,count_dul
                        print 'data:',df.values[j]
        df.to_csv(list_path)
        return df

    def check_results(self,df):
        count = 0
        for i in range(len(df)):
            name = (df['cate_1'].values)[0] + '_' + (df['cate_2'].values)[0] + '_' + (df['cate_3'].values)[0] + '_' + (df['cate_4'].values)[0] + '_' + (df['cate_5'].values)[0]
            name = self.symbol_prune(name)
            try:
                df = pd.read_csv(U'F:/GitHub/Hound_data/'+name+'.csv')
            except:
                count = count + 1
                print '#######################miss:',name
        return count

    def merge_index_gen(self,list_name = 'item_list'):
        list_path = self.list_path + list_name + '.csv'
        df = pd.read_csv(self.list_path)
        df = df.fillna('')

        cates = []
        for i in range(10):
            temp_name = 'cate_'+str(i+1)
            try:
                a = df[temp_name].values()
                cates.append(temp_name)
            except:
                break

        L = len(df)
        item_name = []
        item_catepory = []
        for i in range(L):
            for j in range(len(cates)):
                if j == 0:
                    name = (df[temp_name[j]].values)[i]
                else:
                    name = name+'_'(df[temp_name[j]].values)[i]
            name = self.symbol_prune(name)
            item_name.append(name)

            catepory = (df[temp_name[0]].values)[i]
            catepory = self.symbol_prune(catepory)
            item_catepory.append(catepory)

        df['name'] = item_name
        df['catepory'] = item_catepory

        df_out = pd.DataFrame({'name':[],'category':[]})
        for i in range(len(df)):
            if i == 0:
                df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'category':[df['catepory'].values[i]]}))
            elif len(df_out[df_out['name'] == (df['name'].values)[i]]) == 0:
                df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'category':[df['catepory'].values[i]]}))
            else:
                print i
                print (df['name'].values)[i]
        print len(df_out)
        df_out = df_out.sort_values(by='name')
        df_out.to_csv('test.csv')
        # df_out = pd.read_csv('test.csv')
        # print df_out
        return df_out

    def merge_to_db(self):
        df_out = self.merge_index_gen()
        start_num = 1
        category = '1'
        Last_category = ''
        print len(df_out)
        for i in range(start_num,len(df_out),1):
            try:
                data = pd.read_csv(U'F:/GitHub/Hound_data/'+(df_out['name'].values)[i]+'.csv')
                print 'read'
                Last_category = category
                category = (df_out['category'].values)[i]
                print i
                if i == start_num:
                    df = data
                elif (category != Last_category):
                    print 'save '+Last_category
                    print len(df)
                    MD.create_table(Last_category,df)
                    MD.insert_data(Last_category,df)
                    df = data
                elif i == (len(df_out)-1):
                    print 'last:'
                    print 'save '+Last_category
                    print len(df)
                    df = df.append(data)
                    MD.create_table(Last_category,df)
                    MD.insert_data(Last_category,df)
                else:
                    df = df.append(data)
            except Exception,e:
                print Exception,":",e
                print i,'duplicate'
                print (df_out['name'].values)[i]

                if i == (len(df_out)-1):
                    print 'last:'
                    print 'save '+Last_category
                    print len(df)
                    df = df.append(data)
                    MD.create_table(Last_category,df)
                    MD.insert_data(Last_category,df)

    def merge_to_xls(self):
        df_out = self.merge_index_gen()
        start_num = 1
        category = '1'
        Last_category = ''
        print len(df_out)
        for i in range(start_num,len(df_out),1):
            try:
                data = pd.read_csv(U'F:/GitHub/Hound_data/'+(df_out['name'].values)[i]+'.csv')
                print 'read'
                Last_category = category
                category = (df_out['category'].values)[i]
                print i
                if i == start_num:
                    df = data
                elif (category != Last_category):
                    print 'save '+Last_category
                    print len(df)
                    if len(df) >= 1000000:
                        df_temp = df[0:700000]
                        print 'save 1'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_1.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                        df_temp = df[700000:len(df)]
                        print 'save 2'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_2.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                    else:
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'.xlsx', engine='xlsxwriter')
                        df.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                    df = data
                elif i == (len(df_out)-1):
                    print 'last:'
                    print 'save '+Last_category
                    print len(df)
                    df = df.append(data)
                    if len(df) >= 1000000:
                        df_temp = df[0:700000]
                        print 'save 1'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_1.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                        df_temp = df[700000:len(df)]
                        print 'save 2'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_2.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                    else:
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'.xlsx', engine='xlsxwriter')
                        df.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                else:
                    df = df.append(data)
            except Exception,e:
                print Exception,":",e
                print i,'duplicate'
                print (df_out['name'].values)[i]

                if i == (len(df_out)-1):
                    print 'last:'
                    print 'save '+Last_category
                    print len(df)
                    df = df.append(data)
                    if len(df) >= 1000000:
                        df_temp = df[0:700000]
                        print 'save 1'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_1.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                        df_temp = df[700000:len(df)]
                        print 'save 2'
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'_2.xlsx', engine='xlsxwriter')
                        df_temp.to_excel(writer, sheet_name='Sheet1')
                        writer.save()
                    else:
                        writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_category+'.xlsx', engine='xlsxwriter')
                        df.to_excel(writer, sheet_name='Sheet1')
                        writer.save()