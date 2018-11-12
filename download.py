# _*_ coding:utf-8 _*_ 


'''
用于下载课程

'''
import os,time,json
from My_requests import My_requests
from mooc import get_src


def show_file():

    path=u'lession' ##如果path为unicode，得到的文件名也为unicode；否则，得到文件名编码方式为gbk
    result=os.listdir(path)
    for item in result:
        if 'json' in item:
            # print item
            yield item

# show_file()




def parse_lession_json(path=u'lession',filename=u'my_lession.json'):

    filename=u'%s/%s'%(path,filename)

    with open(filename,'r') as f:
        r=f.read()

    l=r.strip().split('\n')
    for j in l:
        d=json.loads(j)
        yield d


def download(d,path=u'video',lession=None):
    
    folder=u'%s/%s'%(path,lession.split('.')[0])
    if not os.path.exists(folder):
        os.mkdir(folder)

    name=d.keys()[0]
    value=d.values()[0]

    contentType=int(value['contentType'])


    if contentType==1:
        urls=value['urls']
        srcKey=value['srcKey']
        if srcKey:
            src_name=u'%s/%s.src'%(folder,name)

            if not os.path.exists(src_name):
                content=get_src(srcKey=srcKey)
                with open(src_name,'w') as f:
                    print u'download src file,src_name is:%s'%src_name
                    f.write(content)

            else:
                print u'src_name:%s exists!'%src_name
        else:
            print u'cant find srcKey!'



        for i in urls:

            url=i.split('"')[-1]
            extend=url.rsplit('?')[0].rsplit('/',1)[-1]

            if 'mp4' in extend and '_hd' in extend:

                if name:
                    extend=extend.split('.')[-1]
                    filename=u'%s/%s.%s'%(folder,name,extend)
                else:
                    filename=u'%s/%s'%(folder,extend)
               

                print u'new filename is:%s'%filename

                response=My_requests(url=url)

                print u'request url is:',url
                
                if not os.path.exists(filename):


                    content=response.get_content()
                    with open(filename,'wb') as f:
                        print u'download %s......'%filename
                        f.write(content)
                    print u'sleep 60 second'
                    time.sleep(60)
                else:
                   print u'%s exists'%filename

            else:
                print u'only download hd mp4!!!extend is:%s'%extend



    elif contentType==3:

            urls=value['urls']
            for i in urls:

                url=i.split('"')[-1]
                extend=url.rsplit('?')[0].rsplit('/',1)[-1]

               
                if name:
                    extend=extend.split('.')[-1]
                    filename=u'%s/%s.%s'%(folder,name,extend)
                else:
                    filename=u'%s/%s'%(folder,extend)
               

                print u'new filename is:%s'%filename

                response=My_requests(url=url)

                print u'request url is:',url
                
                if not os.path.exists(filename):


                    content=response.get_content()
                    with open(filename,'wb') as f:
                        print u'download %s......'%filename
                        f.write(content)
                    print u'sleep 60 second'
                    time.sleep(60)
                else:
                   print u'%s exists'%filename


    else:
        print u'contentType=%s,name is:%s'%(contentType,name)

            

def main():

    filenames=show_file()

    download_path=u'video'
    json_path='lession'
    if not os.path.exists(download_path):
        os.mkdir(path)

    for filename in filenames:
        print filename
        info=parse_lession_json(path=json_path,filename=filename)

        for d in info:

            download(d=d,path=download_path,lession=filename)


if __name__ =='__main__':

    main()

