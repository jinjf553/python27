#^*^coding:utf-8^*^
#^*^user:jinjf553^*^
#^*^Email:jinjf553@gmail.com^*^
from scrapy import cmdline
cmdline.execute('scrapy crawl movie -o MOaa.csv'.split())