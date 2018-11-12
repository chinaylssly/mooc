# _*_ coding=utf-8 _*_ 
import re
from My_requests import My_requests
import time
import requests
headers=My_requests().headers
print headers

def get_t():
    #unix时间戳，单位毫秒
    return int(time.time()*1000)

s=requests.Session()

login_url='https://reg.icourse163.org/dl/l'
cap_url='https://reg.icourse163.org/dl/cp'
tk_url='https://reg.icourse163.org/dl/gt'


def get_tk(s=s):
    print id(s)

    s.get(url='http://www.icourse163.org/category/all',headers=headers)
    params=dict(
        un='chinaylssly@163.com',
        pkid='cjJVGQM',
        pd='imooc',
        rtid='AUGiHOM8fkTjp4fzz7KgjSjK9uCB5RD3',
        topURL='http=//www.icourse163.org/category/all',
        nocache=get_t(),
        )

    # tk_url='https://reg.icourse163.org/dl/gt?un=chinaylssly%40163.com&pkid=cjJVGQM&pd=imooc&rtid=AUGiHOM8fkTjp4fzz7KgjSjK9uCB5RD3&topURL=http%3A%2F%2Fwww.icourse163.org%2Fcategory%2Fall'
    # params=dict(nocache=get_t())
    # headers=headers
    # res=My_requests(url=tk_url,params=params)
    # res.headers['Referer']='https://reg.icourse163.org/dl/src/mp-agent-finger.html?WEBZJVersion=1530265031808&pkid=cjJVGQM&product=imooc'
    # res.headers['Host']='reg.icourse163.org'
    # print res.headers
    # print res.get_content()

    res=s.get(url=tk_url,params=params,headers=headers,timeout=30)

    print res.content




# get_tk()


def get_cap(s=None):

    # headers=headers
    print id(s)
    params=dict(pd='imooc',
        pkid='cjJVGQM',
        random=get_t(),
        # rtid='AUGiHOM8fkTjp4fzz7KgjSjK9uCB5RD3',
        topURL='http://www.icourse163.org/category/all',
        )

    if s:

        res=s.get(url=cap_url,params=params,headers=headers,timeout=30)
        print res.cookies._cookies
        content=res.content

    else:
        r=My_requests(url=cap_url,params=params)
        print r.get_response().cookies._cookies
        content=r.get_content()

    f=open('cap.png','wb')
    print u'download img .....'
    f.write(content)
    f.close()
    from PIL import Image

    img=Image.open('cap.png')
    img.show()

# get_cap()

def login():

  
    data=dict(
        un="chinaylssly@163.com",
        pw="aUdmvGRtPB4hEGf/NiQblaeI96H3+9qhXKj2PYbzdOu9BwaEOy02Fbzdq9zfp92sa0i7a7Qp/qJc9tSJKN+4baGUIZJNFLDJ2saPh0/zcIFvtkmm1O9HgdhQAbQjoaYghQpsx/BT7CsvYOP7NtEsvdUl369Id7Ku7xtnP6cJnc4=",
        pd="imooc",
        l=1,
        d=10,
        t=1531291987565,
        pkid="cjJVGQM",
        domains="",
        tk="bd0ef694215a7308ffe5aedcbcdb5587",
        pwdKeyUp=0,
        rtid="AUGiHOM8fkTjp4fzz7KgjSjK9uCB5RD3",
        topURL="http=//www.icourse163.org/category/all"
        )
    r=My_requests(url=login_url,method='post',data=data)
    res=r.get_response()
    content=res.content

    print content


login()


def run(s=s):

    get_cap(s=s)

    get_tk(s=s)


