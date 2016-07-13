# -*- coding:utf-8 -*-
import spider_class_ali as sp
import Mult_thread_ctrl as Mt
import agent_fast as ag
import pandas as pd

def data_merge():
    df = pd.read_csv(U'F:/GitHub/Hound/Hound/Hound/data/item_list.csv')

    L = 1000
    df = df[0:L]
    item_name = []
    for i in range(L):
        name = (df['catepory'].values)[i] + '_' + (df['son_catepory'].values)[i] + '_' + (df['gra_son_cate'].values)[i] + '_' + (df['gg_son_cate'].values)[i]
        name = name.replace(' ','')
        name = name.replace("'",'')
        name = name.replace('&','')
        name = name.replace('/','_')
        name = name.replace('"','')
        name = name.replace('*','x')
        item_name.append(name)

    df['name'] = item_name

    df_out = pd.DataFrame({'name':[],'catepory':[],'url':[]})
    for i in range(len(df)):
        if i == 0:
            df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'catepory':[df['catepory'].values[i]],'url':[df['item_url'].values[i]]}))
        elif len(df_out[df_out['name'] == (df['name'].values)[i]]) == 0:
            df_out = df_out.append(pd.DataFrame({'name':[df['name'].values[i]],'catepory':[df['catepory'].values[i]],'url':[df['item_url'].values[i]]}))
        else:
            print i
            print (df['name'].values)[i]
    print len(df_out)


    for i in range(len(df_out)):
        print i
        try:
            data = pd.read_csv(U'F:/GitHub/Hound/Hound/Hound/data/'+(df_out['name'].values)[i]+'.csv')
            Last_catepory = (df_out['catepory'].values)[i-1]
            if i == 0:
                df = data
            elif ((df_out['catepory'].values)[i] != Last_catepory):
                print 'save '+Last_catepory
                print len(df)
                # writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_catepory+'.xlsx', engine='xlsxwriter')
                # df.to_excel(writer, sheet_name='Sheet1')
                # writer.save()
                # df = data
            # elif i == len(df_out)-1:
                # df = df.append(data)
                # writer = pd.ExcelWriter(U'F:/GitHub/category/' + Last_catepory+'.xlsx', engine='xlsxwriter')
                # df.to_excel(writer, sheet_name='Sheet1')
                # writer.save()
            # else:
                # df = df.append(data)
        except:
            print i,'duplicate'

if __name__ == '__main__':
    # ag1 = ag.agent()
    # ag1.run(target='ali',page_num=3,fail_time=2)

    data_merge()



