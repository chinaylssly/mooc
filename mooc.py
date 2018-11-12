# _*_ coding:utf-8 _*_ 
'''
用于获取视频url
'''
from My_requests import My_requests
import time
import re
import os
from cookies import load_cookies,parse_cookies
import json,random

def get_video_info(params0=1007380710,params1=1004513673,contentType=1,csrfKey='9ff7e7f5a962419a83691134fcc541cd',title=None):


    ##不需要cookies
    
    t=time.time()
    print int(t*1000)
    url='http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    data={
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':csrfKey,
        'c0-scriptName':'CourseBean',
        'c0-methodName':'getLessonUnitLearnVo',
        'c0-id':0,
        'c0-param0':'number:%s'%params0,
        'c0-param1':'number:%s'%contentType,
        'c0-param2':'number:0',
        'c0-param3':'number:%s'%params1,
        'batchId':int(t*1000)
        }
    response=My_requests(url=url,method='post',data=data)

    content=response.get_content()

    src_reg=re.compile('nosKey="(.*?)";',re.M)
    srcKey=src_reg.findall(content)

    if srcKey:
        yield srcKey
    else:
        print u'cant find srcKey,will yield response.content'
        yield content

    if int(contentType)==1:
        '''视频'''

        reg=re.compile('\.(.{3,8}Url="http.*?)"')
        s=reg.findall(content)  
        for i in s:
            # print i
            yield i

    elif int(contentType)==3:
        '''课件pdf'''
        print content
        print u'no video url'
        reg=re.compile('http://nos.netease.com/.*?\.pdf',re.M)
        result=reg.findall(content)
        for item in result:
            yield item

    elif int(contentType)==5:
        '''测验'''

        yield None


def get_src(srcKey=None,):

    url='http://www.icourse163.org/video/downloadVideoSrt.htm'
    params=dict(srcKey=srcKey)
    response=My_requests(url=url,params=params,method='get')
    content=response.get_content()
    return content
    


def get_lession_dwr(number=1002788115,cookies=None):
    
    url='http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr'

    httpSessionId=cookies['NTESSTUDYSI']

    data={
        'callCount':1,
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':httpSessionId,##此参数为csrfKey
        'c0-scriptName':'CourseBean',
        'c0-methodName':'getLastLearnedMocTermDto',
        'c0-id':0,
        'c0-param0':'number:%s'%number,
        'batchId':15307  #此参数为时间戳，服务器端不做具体检查,但必须有且需要是整数
        }

    r=My_requests(url=url,method='post',data=data)
    r.headers['Cookie']=parse_cookies(cookies)

    content=r.get_content()
    text=content.decode('unicode-escape').encode('utf-8')
  
    return text




def get_lession_info(dwr):

    reg=re.compile(u'.*?(contentId=.*?);.*?(contentType=.);.*?(id=.*?);.*?name="(.*?)"',re.M)
    result=reg.findall(dwr)

    for item in result:
        contentid=item[0].split('=')[1]
        contentType=item[1].split('=')[1]
        ids=item[2].split('=')[1]
        title=item[3]
       
        if contentid!='null':
            print contentid,ids,title
            yield dict(contentid=contentid,ids=ids,title=title,contentType=contentType)



def write_lession_json(number=1002788115,name=u'中南财经政法大学-中国税制.json', path=u'lession',cookies=None):

   
    filename=u'%s/%s'%(path,name)
    

    if not os.path.exists(filename) or os.path.getsize(filename)==0:
        f=open(filename,'w')

        try:

            dwr=get_lession_dwr(number=number,cookies=cookies)
            info=get_lession_info(dwr=dwr)

            for item in info:
                print item
                params0=item['contentid']
                params1=item['ids']
                csrfKey=cookies['NTESSTUDYSI']
                title=item['title']
                contentType=item['contentType']

                item.pop('title')


                if int(contentType)==1 or int(contentType)==3:

                    result=get_video_info(params0=params0,params1=params1,contentType=contentType,csrfKey=csrfKey,title=title)
                    srcKey=result.next()
                    if isinstance(srcKey,list):
                        srcKey=srcKey[0]
                    else:
                        srcKey=''
                
                    urls=[]
                    for url in result:
                        urls.append(url)
                    item['srcKey']=srcKey
                    item['urls']=urls

                    
                else:

                    print u'pass when contentType=%s'%contentType


                d={title:item}
                j=json.dumps(d,ensure_ascii=False)+'\n'
                f.write(j)

                t=random.choice([0.5,1,1.5,2])

                print u'sleep %s second'%t
                time.sleep(t)

            f.close()


        except Exception,e:
            print u'Exception cause by:',e
            f.close()
            print u'cant get full info,will remove %s'%filename
            os.remove(filename)

            assert 0,u'unexcept error,please restart program!'


    else:

        # os.remove(filename)

        return True

        print u'%s already exists'%filename

def parse_my_lession_json(filename='my_lession.json'):

    with open(filename,'r') as f:
        r=f.read()

        l=r.strip().split('\n')
        for j in l:
            d=json.loads(j)
            
            yield d

def write_all_my_lesssion():

    path=u'lession'
    if not os.path.exists(path):
        os.mkdir(path)

    cookies=load_cookies(flag=2)

    result=parse_my_lession_json()
    for item in result:
        school=item['school']
        name=item['name']
        number=item['ids']

        print school,name,number

        filename=u'%s-%s.json'%(school,name)
        status=write_lession_json(number=number,name=filename,path=path,cookies=cookies)
        if status:
            pass
        else:
            print u'sleep 3 second!'
            time.sleep(3)



if __name__ =='__main__':

    
    write_all_my_lesssion()
    


    pass

