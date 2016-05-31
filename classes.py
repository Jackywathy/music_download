from bs4 import BeautifulSoup as bs
import urllib.request as urllib
import requests
import urllib
import re
audiourl = re.compile(r'audiourl=\".+?')
__author__ = "Jack"
url = "http://mp.weixin.qq.com/s?__biz=MzA4MzY5Mzk1NA==&mid=2656507187&idx=5&sn=e79df6770c8f42adf738504ac84fbb1a&scene=0#wechat_redirect"
site = requests.get(url)
soup = bs(site.text, "html.parser")
tag2 = soup.findAll("qqmusic")
for tag in tag2:
    tag