# -*- coding:utf-8 -*-
import agent as ag
import pandas as pd
import spider_class_ali as sp
import threading
import time
import Mult_thread_ctrl as mt



if __name__ == '__main__':
    thread_num = 8

    M1 = mt.Mult_thread()
    # M1.index_initial(138)
    # M1.get_proxy(target_web = 'ali',proxy_sel='reflash')
    M1.run(thread_num=thread_num,proxy_enable=1,page_max=1000)

    # webdrv=''
    # proxy_ip = get_proxy(target_web='ali',proxy_sel=1)
    # proxy_ip = '123.126.32.102:8080'


