# -*- coding:utf-8 -*-
import spider_class_ali as sp
import Mult_thread_ctrl as Mt
import agent_fast as ag
import pandas as pd

def data_merge():
    # df = pd.read_csv(U'F:/GitHub/Hound_data/item_list.csv')
    # L = len(df)
    # item_name = []
    # item_catepory = []
    # for i in range(L):
    #     name = (df['catepory'].values)[i] + '_' + (df['son_catepory'].values)[i] + '_' + (df['gra_son_cate'].values)[i] + '_' + (df['gg_son_cate'].values)[i]
    #     name = name.replace(' ','')
    #     name = name.replace("'",'')
    #     name = name.replace('&','')
    #     name = name.replace('/','_')
    #     name = name.replace('"','')
    #     name = name.replace('*','x')
    #     name = name.replace('<','')
    #     name = name.replace('>','')
    #     item_name.append(name)
    #
    #     catepory = (df['catepory'].values)[i]
    #     catepory = catepory.replace(' ','')
    #     catepory = catepory.replace("'",'')
    #     catepory = catepory.replace('&','')
    #     catepory = catepory.replace('/','_')
    #     catepory = catepory.replace('"','')
    #     catepory = catepory.replace('*','x')
    #     catepory = catepory.replace('<','')
    #     catepory = catepory.replace('>','')
    #     item_catepory.append(catepory)
    #
    # df['name'] = item_name
    # df['catepory'] = item_catepory
    #
    # df_out = pd.DataFrame({'name':[],'category':[]})
    # for i in range(len(df)):
    #     if i == 0:
    #         df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'category':[df['catepory'].values[i]]}))
    #     elif len(df_out[df_out['name'] == (df['name'].values)[i]]) == 0:
    #         df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'category':[df['catepory'].values[i]]}))
    #     else:
    #         print i
    #         print (df['name'].values)[i]
    # print len(df_out)
    # df_out.sort_values(by='name')
    # df_out.to_csv('test.csv')

    df_out = pd.read_csv('test.csv')
    # print df_out


    #Home,KitchenGarden  986
    start_num = 986
    category = '1'
    Last_category = ''
    print len(df_out)
    for i in range(start_num,len(df_out),1):
        try:
            data = pd.read_csv(U'F:/GitHub/Hound_data/'+(df_out['name'].values)[i]+'.csv')
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


if __name__ == '__main__':
    # ag1 = ag.agent()
    # ag1.run(target='ali',page_num=3,fail_time=2)

    data_merge()



