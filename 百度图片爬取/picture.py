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
url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=\
201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&\
st=-1&z=&ic=0&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&\
qc=&nc=1&fr=&cg=girl&pn={pageNum}&rn=30&gsm=1e00000000001e&1490169411926="

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
    flag += 60

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
    p = re.compile("thumbURL.*?\.jpg")
    print(p)
    #获取正则匹配的结果,返回的是一个list
    s = p.findall(html)
    print(s)
    #如果路径不存在,创建路径,最后的图片保存在此路径下
    if os.path.isdir("E:\\myproject\\MyCrawlPic\\"+Keyword)!=True:
        os.makedirs(r"E:\\myproject\\MyCrawlPic\\"+Keyword)
    with open("testPic1.txt","w") as f:
        for i in s:
            i = i.replace("thumbURL\":\"","")
            print(i)
            f.write(i)
            f.write("\n")
            urllib.request.urlretrieve(i,"E:\\myproject\\MyCrawlPic\\"+Keyword+"\\pic{num}.jpg".format(num=j))
            j += 1
    print(j)
