import scrapy
from spiders.ali_spider import AliSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
  'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(AliSpider(start=0,end=10))
process.start() # the script will block here until the crawling is finished