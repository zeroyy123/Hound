# -*- coding:utf-8 -*-
import spider_class_ali as sp

if __name__ == '__main__':
    thread_num = 10
    sp1 = sp.spider_aliexp()
    sp1.data_reduction()

    # M1 = mt.Mult_thread()
    # # M1.get_proxy(target_web = 'ali',proxy_sel='reflash')
    # M1.run(thread_num=thread_num,proxy_enable=1,page_max=1000)

    # webdrv=''
    # proxy_ip = get_proxy(target_web='ali',proxy_sel=1)
    # proxy_ip = '123.126.32.102:8080'


