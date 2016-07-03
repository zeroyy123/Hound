# -*- coding:utf-8 -*-
import spider_class_ali as sp
import Mult_thread_ctrl as Mt

if __name__ == '__main__':
    # thread_num = 10
    # sp1 = sp.spider_aliexp()
    # sp1.data_reduction()

    # M1 = mt.Mult_thread()
    # # M1.get_proxy(target_web = 'ali',proxy_sel='reflash')
    # M1.run(thread_num=thread_num,proxy_enable=1,page_max=1000)

    # webdrv=''
    Mt1 = Mt.Mult_thread()
    proxy_ip = Mt1.get_proxy(target_web='ali',proxy_sel = 'reflash')
    # proxy_ip = '123.126.32.102:8080'


