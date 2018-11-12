# _*_ coding=utf-8 _*_ 
import re
import requests
import json
import os
import time
from cookies import load_cookies,parse_cookies

'''
获取我的课程
'''

def get_my_lession(p=1,flag=1):
    '''p参数表示页码，flag取值0,1,2！1表示本地载入，2表示网络载入，3表示用户选择本地载入还是网络'''

    url='http://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc'

    data=dict(
            type=30,
            p=p,
            psize=32,
            courseType=1,
            )

    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1'}
    cookies=load_cookies(flag=flag)
    params={'csrfKey':cookies['NTESSTUDYSI']}
    headers['Cookie']=parse_cookies(cookies)
    res=requests.post(url=url,headers=headers,params=params,data=data,timeout=30)

    j=res.json()

    return j



def parse_my_lession(j,p=1):
    '''j为我的课程的json数据，参数p为None时，表示不获取pagecount'''
   
    
    results=j['result']
    result=results['result']
    

    if p==1:
        pagination=results['pagination']
        page=pagination['totlePageCount']
        yield int(page)

    for i in result:

        ids=i['termPanel']['id']
        name=i['name']
        
        schoolPanel=i['schoolPanel']
        school=schoolPanel['name']

        d=dict(ids=ids,name=name,school=school)

        # print d
        yield d

 

def get_my_lession_info():
    ''' 用于获取课程id课程名'''

    filename=u'my_lession.json'

    if os.path.exists(filename):
        os.remove(filename)
        print u'%s exist,so will remove!'%filename

    f=open(filename,'w')

    j=get_my_lession(p=1,flag=2)

    info=parse_my_lession(j=j,p=1)

    page=info.next()

    for i in info:
        txt=json.dumps(i,ensure_ascii=False)+'\n '
        f.write(txt.encode('utf-8'))
    time.sleep(2)
    while page>1:
        j=get_my_lession(p=page,flag=0)
        info=parse_my_lession(j=j,p=page)
        for i in info:
            txt=json.dumps(i,ensure_ascii=False)+'\n'
            f.write(txt.encode('utf-8'))
        time.sleep(2)
        page-=1

    f.close()


if __name__ =='__main__':
    get_my_lession_info()

    pass