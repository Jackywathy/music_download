from bs4 import BeautifulSoup as bs
import urllib.request as url3
import requests
__author__ = "Jack"
url = "http://mp.weixin.qq.com/s?__biz=MzA4MzY5Mzk1NA==&mid=2656507187&idx=5&sn=e79df6770c8f42adf738504ac84fbb1a&scene=0#wechat_redirect"
url = "http://mp.weixin.qq.com/s?__biz=MjM5NDQ0MzIxNw==&mid=2655053804&idx=1&sn=cd76a9891ae482198556909aa2bbaa05&scene=0#rd"
site = requests.get(url)
soup = bs(site.text, "html.parser")
tag2 = soup.findAll("qqmusic")
errors = []
for tag in tag2:
    try:
        req = url3.Request(tag['audiourl'], headers={'User-Agent':"Firefox/2.0.0.11"})
        file_name = tag['music_name']
        u = url3.urlopen(req, timeout=45)
        f = open(file_name + '.m4a', 'wb')
        meta = u.info()
        print(str(meta).replace('\n','|'))
        file_size = int(meta["Content-Length"])
        print("Downloading: %s Bytes: %s" % (file_name, file_size))
        file_size_dl = 0
        block_sz = 65536
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%6.2f%%] [%10s]" % (file_size_dl, file_size_dl * 100. / file_size,'-'* int(file_size_dl * 10 / file_size))
            print(status)

        f.close()
    except url3.socket.timeout:
        errors.append((file_name, tag['audiourl']))
        continue

print("DONE")
with open('error.txt','w') as w:
    for i in w:
        print(i[0],i[1], file=w)
