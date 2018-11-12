# _*_ coding:utf-8 _*_ 


'''

选择cookies加载方式


'''

from login import login
from wait import wait
import json,os



def load_cookies(flag=2):
    '''选择载入cookies方式，默认为本地载入'''
    assert flag in [0,1,2],u'flag=0表示从本地载入cookies，flag=1表示从网络载入cookies，flag=3表示用户选择从网络还是本地载入cookies'

    if flag==2:

        message=u'load cookies from internet please input any key\nfrom location please click ENTER key:'
        p=wait(timeout=5,message=message)

        if p:
            cookies=login()
            write_cookies(cookies=cookies)
        else:
            cookies=read_cookies()

    elif flag==1:
        cookies=login()
        write_cookies(cookies=cookies)

    elif flag==0:
        cookies=read_cookies()

    return cookies



def write_cookies(cookies):
    '''将网络cookies写入本地'''

    j=json.dumps(cookies,ensure_ascii=False)
    print u'write cookies dict into cookies.json......'
    with open('cookies.json','w')as f:
        f.write(j)

def read_cookies():
    '''从本地载入cookies '''

    if not os.path.exists('cookies.json'):
        assert 0,u'localtion cookies.json doest exists,please load cookies from internet'

    with open('cookies.json','r') as f:
        r=f.read()

    cookies=json.loads(r)

    return cookies


def parse_cookies(cookies):
    '''字典形式cookies转化成字符串，以便于放入headers中'''
    s=''
    for i in cookies.items():
        k=str(i[0])+'='+str(i[1])+';'
        s+=k

    return s




if __name__=='__main__':

    load_cookies(flag=1)