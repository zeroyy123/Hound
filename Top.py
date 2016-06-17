# -*- coding:utf-8 -*-
import agent as ag
import pandas as pd
import spider_class as sp






def get_item_count():
    index_table = pd.read_csv('ali_cate_list.csv')
    print 'table length : ',len(index_table)

    if target_web == 'ali':
        sp1 = sp.spider_aliexp()
    elif target_web == 'amz':
        sp1 = sp.spider_amz()

    result_count = []
    sp1.open_web_driver(proxy_ip)
    for n in range(len(index_table)):
        print n
        category = index_table['category'].values[n]
        sub_cate = index_table['sub_cate'].values[n]
        item = index_table['item'].values[n]

        target = category + '_' + sub_cate + '_' + item
        print target   
        target_url = index_table['url'].values[n]
        sp1.open_web_url(target_url)
        count = sp1.get_search_count()
        result_count.append(count)
        print count
        
    sp1.driver_quit()

    index_table['item_count'] = result_count
    index_table.to_csv('ali_cate_list.csv',encoding='utf-8')
    writer = pd.ExcelWriter('ali_cate_list'+'.xlsx', engine='xlsxwriter')
    index_table.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def get_item_detail(target_web,proxy_ip,webdrv):
    index_table = pd.read_csv('ali_cate_list.csv')
    L = len(index_table)
    target_num = 1000
    print 'table length : ',L

    for i in range(69,L,1):  # have bug
        print 'title_num:',i
        n = i
        category = index_table['category'].values[n]
        sub_cate = index_table['sub_cate'].values[n]
        item = index_table['item'].values[n]

        target = category + '_' + sub_cate + '_' + item
        target = target.replace("’","")
        target_url = index_table['url'].values[n]
        print target
        print target_url

        if target_web == 'ali':
            sp1 = sp.spider_aliexp()
        elif target_web == 'amz':
            sp1 = sp.spider_amz()

        sp1.process(target=target,proxy_ip=proxy_ip,webdrv = webdrv,target_num=target_num,url=target_url)

def get_proxy(target_web):
    Ag = ag.agent()
    Ag.mult_verify(target_web,10,2)

    proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
    proxy_ip = (proxy_ip['ip_addr'].values)[0]
##    proxy_ip = '175.25.25.134:8118'
##    proxy_ip = ''
    print proxy_ip
    return proxy_ip

if __name__ == '__main__':
    
    target_web = 'ali'
##  proxy_ip = get_proxy(target_web)
    proxy_ip = ''
    webdrv   = 'PhantomJS'
    get_item_detail(target_web,proxy_ip,webdrv)
    
##    index_table = pd.read_csv('ali_cate_list.csv')
##    count = index_table['item_count'].values
##    sum_count = 0
##    for i in range(len(count)):
##        if count[i] != 'none':
##            count[i] = count[i].replace(',','')
##            sum_count = sum_count + int(count[i])
##        
##    print sum_count
##    print (13*sum_count/4500)/60
    
