# -*- coding:utf-8 -*-
import threading
import time

import pandas as pd

import others.spider_class_ali as sp
from others import agent as ag


class Mult_thread():
    def __init__(self):
        self.mutex = threading.Lock()

        index_table = pd.read_csv('data/ali_cate_list.csv')
        del index_table['Unnamed: 0']
        state = index_table['state'].values
        L = len(state)
        for i in range(L):
            if state[i] == 'busy':
                state[i] = 'idle'
        index_table['state'] = state
        index_table.to_csv('data/ali_cate_list.csv')
        print index_table.tail(5)

##        self.obj = obj

    def index_initial(self,num):
        index_table = pd.read_csv('data/ali_cate_list.csv')
        del index_table['Unnamed: 0']
        state = []
        for i in range(len(index_table)):
            if i < num:
                state.append('finish')
            else:
                state.append('idle')
        index_table['state'] = state
        index_table.to_csv('data/ali_cate_list.csv')
    
    def get_idle_target(self):
        if self.mutex.acquire(1):
            index_table = pd.read_csv('data/ali_cate_list.csv')
            del index_table['Unnamed: 0']
            state = index_table['state'].values
            L = len(state)
            for i in range(L):
                if state[i] == 'idle':
                    category = index_table['category'].values[i]
                    sub_cate = index_table['sub_cate'].values[i]
                    item = index_table['item'].values[i]
                    target_url = index_table['url'].values[i]
                    state[i] = 'busy'
                    break
                if i == L-1:
                    return ['','',0,'none']
            index_table['state'] = state
            index_table.to_csv('data/ali_cate_list.csv')
            self.mutex.release()
        target = category + '_' + sub_cate + '_' + item
        target = target.replace("’","")
        index = i
        return [target,target_url,index,'success']
    
    def set_finish_target(self,target_num):
        print 'mark 2'
        if self.mutex.acquire(1):
            print 'mark 3'
            index_table = pd.read_csv('data/ali_cate_list.csv')
            del index_table['Unnamed: 0']
            state = index_table['state'].values
            state[target_num] = 'finish'
            index_table['state'] = state
            index_table.to_csv('data/ali_cate_list.csv')
            self.mutex.release()
        else:
            print 'mutex.acquire fail'

    def set_idle_target(self,target_num):
        if self.mutex.acquire(1):
            print 'idle mark'
            index_table = pd.read_csv('data/ali_cate_list.csv')
            del index_table['Unnamed: 0']
            state = index_table['state'].values
            state[target_num] = 'idle'
            index_table['state'] = state
            index_table.to_csv('data/ali_cate_list.csv')
            self.mutex.release()

    def get_item_detail(self,proxy_ip,webdrv,target_sel,page_max):
        [target,target_url,index,flag] = self.get_idle_target()
        print target
        print target_url
        if flag == 'success':
##            sp1 = self.obj
            sp1 = sp.spider_aliexp()
            try:
                sp1.process(target=target,proxy_ip=proxy_ip,webdrv = webdrv,page_max=page_max,url=target_url)
                print 'mark'
                self.set_finish_target(index)
            except:
                self.set_idle_target(index)
                print target
                print target_url
                print 'target: ', index, ' error'
            return 'sub finish'
        else:
            return 'all finish'
        
    def get_proxy(self,target_web,proxy_sel):
        if proxy_sel == 'disable':
            proxy_ip = ''
        elif proxy_sel == 'reflash':
            Ag = ag.agent()
            Ag.mult_verify(target_web,3,2)
            proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
            proxy_ip = (proxy_ip['ip_addr'].values)[0]
        else:
            proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
            proxy_ip = (proxy_ip['ip_addr'].values)[proxy_sel]

        print proxy_ip
        return proxy_ip
    
    def sub_thread(self,target_web,proxy_sel,webdrv,target_sel,page_max):
        proxy_ip = self.get_proxy(target_web=target_web,proxy_sel=proxy_sel)
        while 1:
            flag = self.get_item_detail(proxy_ip=proxy_ip,webdrv=webdrv,target_sel=target_sel,page_max=page_max)
            if flag == 'all finish':
                break
            
    def run(self,thread_num=1,proxy_enable=0,webdrv='PhantomJS',page_max = 1000):
        target_web = 'ali'
        thrs = []

        print 'page_max: ',page_max

        for i in range(thread_num):
            if proxy_enable == 0:
                proxy_sel = 'disable'
            else:
                proxy_sel = i
                
            target_sel = ''
            t = threading.Thread(target = self.sub_thread, args = (target_web,proxy_sel,webdrv,target_sel,page_max))
            thrs.append(t)

        for t in thrs:
            time.sleep(1)
            t.setDaemon(True) #保护进程不要在主进程结束后 也被结束
            t.start()

        for t in thrs:
            t.join()
