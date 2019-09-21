import re
import urllib.request
import sys
import os
from bs4 import BeautifulSoup
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


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

def useWebEngineMethod(url):
    global dir_name2
    global img_name
    webBrowser = MyWebBrowser()
    html = webBrowser.downloadHtml(url)
    # print(html)
    re_img = '<a href="(.*?)" title="查看原图".*?'
    img = re.findall(re_img,html) # 图片列表
    # print(data)
    soup = BeautifulSoup(html,'lxml')
    for h2 in soup.select('h2'):
        dir_name = h2.get_text()
        dir_name2 = dir_name.replace("\n","").rstrip() # 去除回车及空格
        os.mkdir(dir_name2) # 创建文件夹
    num = 1
    for img_url in img:
        img_name = str(num) + '.jpg'
        print(img_name)
        img_dir = dir_name2 + '\\' + img_name
        urllib.request.urlretrieve(img_url, img_dir)
        num = num + 1

if __name__=='__main__':
    url = "https://www.toutiao.com/a6737947689629041155/"
    useWebEngineMethod(url)