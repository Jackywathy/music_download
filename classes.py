from bs4 import BeautifulSoup as bs
import urllib.request as url3
import requests
__author__ = "Jack"


url = "http://mp.weixin.qq.com/s?__biz=MzA4MzY5Mzk1NA==&mid=2656507187&idx=5&sn=e79df6770c8f42adf738504ac84fbb1a&scene=0#wechat_redirect"
url = "http://mp.weixin.qq.com/s?__biz=MjM5NDQ0MzIxNw==&mid=2655053804&idx=1&sn=cd76a9891ae482198556909aa2bbaa05&scene=0#rd"
site = requests.get(url)
soup = bs(site.text, "html.parser")
tag2 = soup.findAll("qqmusic")
for tag in tag2:
    #req = url3.Request(tag['audiourl'], headers={'User-Agent':"Firefox/2.0.0.11"})
    print(tag['music_name'])
    
    url3.urlretrieve(tag['audiourl'],tag['music_name']+'.m4a')