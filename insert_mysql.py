# _*_ coding:utf-8 _*_ 
import json,os,time

def show_file():
    path='json'
    # os.chdir(path)
    result=os.listdir(path)
    for i in result:
        yield u'json/%s'%i.decode('gbk','ignore')



def load_json(filename=u'json/计算机-1001043131.json'):

    f=open(filename,'r')
    r=f.read()
    f.close()
    l=r.strip().split('\n')

    for i in l:
        j=json.loads(i)
        yield j

def parse_json(j):
    school=j['school']
    name=j['name']
    ids=j['ids']
    summary=j['jsonContent']


    # print school
    # print name
    # print ids
    # print summary
    # # assert 0

    # print u'\n'

    return dict(school=school,name=name,ids=ids,summary=summary)


    # break


def main():
    from mysql import mysql

    filenames=show_file()
    for filename in filenames:
        result=load_json(filename=filename)
        for j in result:
            info=parse_json(j=j)
            info['refer']=filename.split('-')[0].split('/')[-1]

            print json.dumps(info,ensure_ascii=False)
            mysql().insert_category(info)


if __name__ == '__main__':

    # main()