from bs4 import BeautifulSoup as bs
import urllib.request as url3
import requests
import os
import re
import time
import datetime
__author__ = "Jack"
#url2 = "http://mp.weixin.qq.com/s?__biz=MzIzNzAxMDI1Nw==&mid=2655445873&idx=1&sn=c938d1829e1d8b7e84818fcebd6a4c6d&scene=0#rd"
#url1 = "http://mp.weixin.qq.com/s?__biz=MzIzNzAxMDI1Nw==&mid=2655445807&idx=2&sn=722ea56916e8a597dc54a41695e92c91&scene=0#rd"
url1 = "http://mp.weixin.qq.com/s/ovS_vHlazFe3ov1jK0zl3A"


def download_qq(qq_link):

    site = requests.get(qq_link)
    soup = bs(site.text, "html.parser")
    tag2 = soup.findAll("qqmusic")
    errors = []
    path = assign_folder()
    


    for tag in tag2:
        now = datetime.datetime.now()
        req = url3.Request(tag['audiourl'], headers={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"})
        file_name = tag['music_name']
        print(file_name + '.m4a')
        if os.path.isfile(os.path.join(path, file_name + '.m4a')):
            print(file_name, 'already found')
            continue
        try:
            u = url3.urlopen(req, timeout=200)
            with open(os.path.join(path, file_name + '.m4a'), 'wb') as f:
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
                    status = r"%10d  [%6.2f%%] [%-10s]" % (file_size_dl, file_size_dl * 100. / file_size,'-' * int(file_size_dl * 10 / file_size))
                    print(status)

        except url3.socket.timeout:
            errors.append((file_name, tag['audiourl']))
            print("ERROR TIMEOUT", file_name,tag['audiourl'])
            continue
        
        print('time taken:', (datetime.datetime.now()-now).seconds)
        time.sleep(1)

    print("DONE")
    
    with open('error%s.txt' % path,'w',encoding='UTF-8') as w:
        for i in errors:
            print(i[0], i[1], file=w)

mp3 = re.compile(r'location\.href=.*?;')


def _download_link(broken_link):
    link = 'http://m.9ku.com'+broken_link
    site = requests.get(link)
    return ((mp3.findall(site.text))[0].split('"')[1])



def assign_folder():
    path = 1
    #TODO REMOVE!
    return str(path)
    while os.path.exists(str(path)):
        path += 1
    path = str(path)
    os.mkdir(path)
    return str(path)

def download_9ku(link, skips=0):
    site = requests.get(link)
    soup = bs(site.content, "html.parser")

    path = assign_folder()
    errors = 'errors%s.txt' % path
    for tag in soup.findAll('span', class_='t-t'):
        for i in tag.a:
            if skips:
                skips -= 1
                continue
            down_link = _download_link(tag.a.get('href'))
            req = url3.Request(down_link, headers={'User-Agent': "Firefox/2.0.0.11"})
            file_name = i
            if os.path.isfile(path+'\\' + file_name+'.mp3'):
                print("Already downloaded")
                continue

            try:
                u = url3.urlopen(req, timeout=500)
                with open(path + '\\' + file_name + '.mp3', 'wb') as f:
                    meta = u.info()
                    print(str(meta).replace('\n', '|'))
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
                        status = r"%10d  [%6.2f%%] [%-10s]" % (
                        file_size_dl, file_size_dl * 100. / file_size, '-' * int(file_size_dl * 10 / file_size))
                        print(status)

            except url3.socket.timeout:
                with open(errors,'a') as f:
                    f.write(str(file_name) + str(down_link))
                    print("ERROR TIMEOUT", file_name, down_link)
                    continue







#download_9ku('http://m.9ku.com/laoge/500shou.htm',11)
download_qq(url1)


    #download_qq('http://mp.weixin.qq.com/s?__biz=MjM5NTQ2ODgzMg==&mid=405099049&idx=1&sn=4291547f9803d4877ed28cad0e37a131&scene=0#rd')
