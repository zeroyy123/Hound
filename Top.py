import agent as ag
import pandas as pd
import spider_class as sp



target_web = 'ali'


# sp1 = sp.spider_aliexp()
#
# proxy_ip = ''
# sp1.open_web(proxy_ip)
# sp1.get_index()

# Ag = ag.agent()
# Ag.mult_verify(target_web,10,2)

# proxy_ip = pd.read_csv(target_web+'_proxy_ip.csv')
# proxy_ip = (proxy_ip['ip_addr'].values)[0]
# # # proxy_ip = '175.25.25.134:8118'
proxy_ip = ''
# print proxy_ip
index_table = pd.read_csv('ali_cate_list.csv')
print 'table length : ',len(index_table)
n = 2
# n = 1
category = index_table['category'].values[n]
sub_cate = index_table['sub_cate'].values[n]
item = index_table['item'].values[n]
# target = 'Num_'+str(n)+'_'+item
target = category + ' ' + sub_cate + ' ' + item
target_url = index_table['url'].values[n]
print target
print target_url

if target_web == 'ali':
    sp1 = sp.spider_aliexp()
elif target_web == 'amz':
    sp1 = sp.spider_amz()

sp1.process(target=target,proxy_ip=proxy_ip,target_num=2,url=target_url)


