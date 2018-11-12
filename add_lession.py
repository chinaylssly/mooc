# _*_ coding:utf-8 _*_ 


'''
将课程添加至我的学习
'''

from My_requests import My_requests
from cookies import load_cookies,parse_cookies
import json
import re,time


def add_lession(tid=1002977006):

    url='http://www.icourse163.org/dwr/call/plaincall/CourseBean.startTermLearn.dwr'

    cookies=load_cookies(flag=1)
    csrfKey=cookies['NTESSTUDYSI']

    cookies=parse_cookies(cookies=cookies)

    data={
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':csrfKey,
        'c0-scriptName':'CourseBean',
        'c0-methodName':'startTermLearn',
        'c0-id':0,
        'c0-param0':'string:%s'%tid,
        'c0-param1':'null:null',
        'batchId':1531726020251,
        }

    r=My_requests(url=url,method='post',data=data)
    r.headers['Cookie']=cookies

    content=r.get_content()

    reg=re.compile('\((.*?)\)')

    result=reg.findall(content)

    print result

    if result:
        '''
        "'1531726020251','0',1374827585"
        result 为以上形式表示添加课程成功

        '''
        result=result[0]
        l=result.split(',')

        for i in l:
            try:
                int(i.replace("'",''))

            except:
                print u'add lession failed!可能原因：该课程已关闭'
                print result
                return False
        print u'add lession successfully!'
        return True

    else:
        print u'add lession failed,可能原因：该课程已关闭'
        print result
        return False




if __name__=='__main__':
    # add_lession(1002785027)
    add_lession(1002923009)
    pass