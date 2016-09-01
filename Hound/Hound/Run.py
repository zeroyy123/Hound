import scrapy
import spiders.ali_spider as ali_spider

import spiders.ali_list_spider as ali_list_spider
from scrapy.crawler import CrawlerProcess
import BaseCtrl as BC
import pandas as pd

process = CrawlerProcess({
  'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

BC = BC.BaseCtrl()

#update index
BC.set_pipelines('ali_list_spider')
process.crawl(ali_list_spider.AliSpider())
process.start() # the script will block here until the crawling is finished

#duplicate index

df = BC.list_duplicate_delete(list_name = 'item_list')

#start crawl
L = len(df)
count = BC.check_results(df)
last_count = count

BC.set_pipelines('ali_spider')
while(count!=0):
  process.crawl(ali_spider.AliSpider(start=0,end=L))
  process.start()
  last_count = count
  count = BC.check_results(df)
  if count == last_count:
    break

# merge data to database
BC.merge_to_db()
