# coding:utf-8
# 微信：15538135475
import re
import json
import pymongo
from selenium import webdriver
from multiprocessing.pool import Pool

client = pymongo.MongoClient('localhost')
db = client['maoyan']

driver = webdriver.PhantomJS()
driver.set_window_size(1400,900)

def get_one_page(url):
    driver.get(url)
    try:
        html = driver.page_source
        if html:
            return html
        return None
    except Exception:
        print('出错了。')
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
            }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def save_to_mongo(result):
    try:
        if db['maoyan'].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储失败')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        save_to_mongo(item)
        #write_to_file(item)

if __name__ == '__main__':
    for i in range(0,10):
        main(i)
