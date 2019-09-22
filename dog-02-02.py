import re
import urllib.request
import sys
import os
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

get_num = 10 # 爬取的次数，可自行修改

class MyWebBrowser(QWebEnginePage):
    app = None
    def __init__(self):
        if MyWebBrowser.app is None:
            MyWebBrowser.app = QApplication(sys.argv)
        super().__init__()
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)

    def downloadHtml(self, url):
        self.load(QUrl(url))
        print("\n正在下载网页源码：", url)
        MyWebBrowser.app.exec_()
        return self.html

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)

    def Callable(self, html_str):
        self.html = html_str
        MyWebBrowser.app.quit()


def safe_img(html):
    global dir_name2
    global img_name
    re_img = '<a href="(.*?)" title="查看原图".*?'
    img = re.findall(re_img,html) # 图片列表
    print(img)
    soup = BeautifulSoup(html,'lxml')
    for h2 in soup.select('h2'):
        dir_name = h2.get_text()
        dir_name2 = dir_name.replace("\n","").rstrip() # 去除回车及空格
        os.mkdir(dir_name2) # 创建文件夹
        with open("ImgNameLog.txt",'a+',encoding="utf-8") as f:
            f.write(dir_name2 + "\n")
            f.close()
    num = 1
    for img_url in img:
        img_name = str(num) + '.jpg'
        print(img_name)
        img_dir = dir_name2 + '\\' + img_name
        urllib.request.urlretrieve(img_url, img_dir)
        num = num + 1

def get_next_name(html):
    list_name = []
    doc = pq(html)
    data = doc('.img-title-inner span').items() # 为什么只能获取到5个
    for i in data:
        list_name.append(i.text())
    # print(list_name)
    return list_name

def get_next_url(html):
    # 跳转
    re_next = '<a href="(.*?)"><div class="img-wrap">.*?'
    list_url = re.findall(re_next,html)
    # print(list_url)
    return list_url

def dict_next(html):
    global c
    a = get_next_name(html)
    b = get_next_url(html)
    c = dict(zip(a,b))
    # print(c)


def inquire_file(c):
    data = open("ImgNameLog.txt",'r',encoding="utf-8")
    data_name = data.readlines()
    # print(data_name)
    while True:
        for y in c:
            if os.path.exists(y):
                print(y + "已爬取，跳过")
                continue
            else:
                print("开始爬取:" + y)
                return True,y

def useWebEngineMethod(url):
    global get_num
    if get_num > 0:
        get_num = get_num - 1
        time.sleep(3) # 爬取页面后等待时间（3秒），可自行修改
    else:
        exit()
    webBrowser = MyWebBrowser()
    html = webBrowser.downloadHtml(url)
    # print(html)
    safe_img(html)
    dict_next(html)
    data1 = inquire_file(c)[1]
    url = c[data1]
    return useWebEngineMethod(url)


if __name__=='__main__':
    with open('ImgNameLog.txt','w+',encoding='utf-8') as f:
        f.write('start\n')
        f.close()
    url = "https://www.toutiao.com/a6737947689629041155/"
    useWebEngineMethod(url)