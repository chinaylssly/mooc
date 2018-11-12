# _*_ coding:utf-8 _*_ 
'''
用于获取慕课网所有视频信息

'''
import requests
import json
import re,time,os


headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

def get_session():

    s= requests.Session()
    url='http://www.icourse163.org/category/all'
    response=s.get(url=url,headers=headers)
    cookies=response.cookies

    # print help(cookies)

    value=cookies.get('NTESSTUDYSI')

    # value=cookies.values()[0].values()[0]['NTESSTUDYSI']
    # value=str(value).split('=')[-1].split(' ')[0]
 
    return dict(s=s,csrfKey=value)



def get_lession(pageIndex=1,categoryId=1001043131,order=0,d=None):

    csrfKey=d['csrfKey']
    s=d['s']
    params=dict(csrfKey=csrfKey)
    url='http://www.icourse163.org/web/j/courseBean.getCoursePanelListByFrontCategory.rpc'

    data=dict(
        categoryId=categoryId,
        type=30,
        orderBy=order,
        pageIndex=pageIndex,
        pageSize=20,
        )
    r=s.post(url=url,data=data,headers=headers,params=params)
    
    return r.json()



def parse_json(p=1,content=None):
    
    result=content['result']
    if p==1:
        pagination=result['pagination']
        pagecount=pagination['totlePageCount']
        print pagecount
        yield int(pagecount)

    result=result['result']
    for item in result:
        name=item['name']
        schoolPanel=item['schoolPanel']
        school=schoolPanel['name']

        termPanel=item['termPanel']
        ids=termPanel['id']
        jsonContent=termPanel['jsonContent'].strip()

        print school,name,ids
        print jsonContent
        print '\n'

        yield dict(school=school,name=name,ids=ids,jsonContent=jsonContent)





def get_lession_by_category(info={'categoryid':'1001043131','categoryname':u'计算机'}):
    name=info['categoryname']
    categoryId=info['categoryid']
    print u'currrent category is:%s,id is:%s'%(name,categoryId)
    d=get_session()
    content=get_lession(pageIndex=1,d=d,categoryId=categoryId)
    result=parse_json(content=content)
    pagecount=result.next()
    for item in result:
        yield item
    print u'sleep 20 second!'
    time.sleep(20)

    for page in range(2,pagecount+1):
        content=get_lession(pageIndex=page,d=d,categoryId=categoryId)
        result=parse_json(p=page,content=content)
        for item in result:
            yield item
        print u'sleep 20 second!'
        time.sleep(20)





def get_category():

    d=get_session()
    assert isinstance(d,dict) ,u'params d is not dict'
    url='http://www.icourse163.org/web/j/mocCourseCategoryBean.getCategByType.rpc'
    params=dict(csrfKey=d['csrfKey'])
    s=d['s']
    data={'type':4}
    r=s.post(url=url,data=data,params=params,headers=headers,timeout=30)
    content=r.json()
    result=content['result']
    for item in result:
        print item['id'],item['name'],item['linkName']
        yield dict(categoryid=item['id'],categoryname=item['name'])



def write_category():

    category_info=get_category()
    for info in category_info:
        filename=u'%s-%s.json'%(info['categoryname'],info['categoryid'])
        # filename=filename.encode('utf-8','ignore')
        if not os.path.exists(filename) or os.path.getsize(filename)==0:
            try:
                f=open(filename,'w')
                print u'create json file:%s'%filename
                result=get_lession_by_category(info=info)
                for item in result:
                    j=json.dumps(item,ensure_ascii=False)+'\n'
                    f.write(j.encode('utf-8','ignore'))
                f.close()

            except Exception,e:
                print u'exception cause by:',e
                print u'cant get full info will remove %s'%filename
                f.close()
                os.remove(filename)
                break



        else:
            print u'json file:%s exists'%filename



if __name__=='__main__':

    # write_category()
    pass