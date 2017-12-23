from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from config import *
from hashlib import md5
from multiprocessing.pool import Pool,RemoteTraceback
from json.decoder import JSONDecodeError
import requests
import json
import re
import pymongo
import os

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page_index(offset,keyword):
    data = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
        'from':'gallery'
        }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except RemoteTraceback:
        print(None)
        pass

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错',url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile('gallery: JSON\.parse\("(.*?)"\)')
    result = re.search(images_pattern,html)
    if result:
        try:
            data = json.loads(result.group(1).replace('\\',''))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                for image in images: download_image(image)
                return {
                    'title':title,
                    'url':url,
                    'images':images
                    }
        except JSONDecodeError:
            print('JSONDecodeError')
        
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功')
            return True
        return False
    except:
        print('NoneType')

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content,url)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content,url):
    print('正在下载：',url)
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html = get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        html= get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result: save_to_mongo(result)

if __name__ == '__main__':
    
    groups = [x*20 for x in range(GROUP_START,GROUP_END + 1)]
    pool = Pool()
    pool.map(main,groups)

    
