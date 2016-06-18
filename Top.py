# -*- coding:utf-8 -*-
import agent as ag
import pandas as pd
import spider_class_ali as sp
import threading
import time


def get_item_count(proxy_ip):
    index_table = pd.read_csv('data/ali_cate_list.csv')
    print 'table length : ',len(index_table)
    sp1 = sp.spider_aliexp()

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

def get_item_detail(target_web,proxy_ip,webdrv,target_sel,target_num):
    index_table = pd.read_csv('data/ali_cate_list.csv')
    L = len(index_table)

    print 'table length : ',L

    if target_web == 'ali':
            sp1 = sp.spider_aliexp()
    elif target_web == 'amz':
        sp1 = sp.spider_amz()


    if target_sel == '':
        for i in range(70,L,1):
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

            sp1.process(target=target,proxy_ip=proxy_ip,webdrv = webdrv,target_num=target_num,url=target_url)
    else:
        n = target_sel
        category = index_table['category'].values[n]
        sub_cate = index_table['sub_cate'].values[n]
        item = index_table['item'].values[n]

        target = category + '_' + sub_cate + '_' + item
        target = target.replace("’","")
        target_url = index_table['url'].values[n]
        print target
        print target_url

        sp1.process(target=target,proxy_ip=proxy_ip,webdrv = webdrv,target_num=target_num,url=target_url)

def get_proxy(target_web,proxy_sel):
    if proxy_sel == 'disable':
        proxy_ip = ''
    elif proxy_sel == 'reflash':
        Ag = ag.agent()
        Ag.mult_verify(target_web,10,2)
        proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
        proxy_ip = (proxy_ip['ip_addr'].values)[0]
    else:
        proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
        proxy_ip = (proxy_ip['ip_addr'].values)[proxy_sel]

    print proxy_ip
    return proxy_ip

def sub_thread(target_web,proxy_sel,webdrv,target_sel,target_num):
    proxy_ip = get_proxy(target_web=target_web,proxy_sel=proxy_sel)
    get_item_detail(target_web=target_web,proxy_ip=proxy_ip,webdrv=webdrv,target_sel=target_sel,target_num=target_num)

def mult_thread(thread_num,start_num,proxy_enable,target_num = ''):
    webdrv   = 'PhantomJS'
    target_web = 'ali'
    thrs = []

    if target_num == '':
        target_num = 1000

    print 'page_target_num: ',target_num

    for i in range(thread_num):
        if proxy_enable == 0:
            proxy_sel = 'disable'
        else:
            proxy_sel = i

        target_sel = start_num + i
        t = threading.Thread(target = sub_thread, args = (target_web,proxy_sel,webdrv,target_sel,target_num))
        thrs.append(t)

    for t in thrs:
        time.sleep(1)
        t.setDaemon(True) #保护进程不要在主进程结束后 也被结束
        t.start()

    for t in thrs:
        t.join()

if __name__ == '__main__':
    thread_num = 1
    mult_thread(thread_num=thread_num,start_num=70, proxy_enable=0,target_num=2)


