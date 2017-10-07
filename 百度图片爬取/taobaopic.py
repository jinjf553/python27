# encoding:utf-8

import urllib.request
import urllib.parse
import re
import os

#伪装成浏览器进行访问
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
                  537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                     "referer":"https://image.baidu.com"}
#url
url = "https://s.taobao.com/search?q={word}&imgfile=&commend=all&ssid=s5-e&search_type=item\
&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20171003\
&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s={pageNum}"

#搜索图片的关键字
Keyword = input("请输入关键字:")
#转换编码格式
keyword = urllib.parse.quote(Keyword,"utf-8")
#用于条件判断
flag = 0
#j作为写入图片的识别标志,默认从第0张开始,每写入一张j就+1
j = 0

error = 0

#获取前3000张图片
while(flag < 150):
    flag += 44

    #url链接
    url1 = url.format(word = keyword,pageNum = str(flag))
    print(url1)
    #获取请求
    rep = urllib.request.Request(url1,headers=header)
    print(rep)
    #打开网页
    rep = urllib.request.urlopen(rep)
    print(rep)
    html = None
    #读取网页数据
    try:
        html = rep.read().decode("utf-8")
    except:
        print("something wrong!")
        error = 1
        print("-------------now page =" + str(flag))
    if(error == 1):
        continue
    #正则匹配,..
    p = re.compile("pic_url.*?\.[jpgS][pniS][gf2]")
    print(str(p)+"1111111111111111")
    #获取正则匹配的结果,返回的是一个list
    s = p.findall(html)
    print(s)
    #如果路径不存在,创建路径,最后的图片保存在此路径下
    if os.path.isdir("E:\\myproject\\MyCrawlPic\\"+Keyword)!=True:
        os.makedirs(r"E:\\myproject\\MyCrawlPic\\"+Keyword)
    with open("testPic1.txt","w") as f:
        for i in s:
            i = i.replace("pic_url\":\"","http:")
            print(i)
            f.write(i)
            f.write("\n")
            try:
                urllib.request.urlretrieve(i,"E:\\myproject\\MyCrawlPic\\"+Keyword+"\\pic{num}.jpg".format(num=j))
            except:
                continue
            j += 1
    print(j)
