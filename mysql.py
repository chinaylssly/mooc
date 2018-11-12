# _*_ coding:utf-8 _*_ 

from My_MySQL import MySQL

class mysql(MySQL):
    def __init__(self,):
        super(mysql,self).__init__(db='mooc')

    def test(self,):
        query='show tables'
        data=self.execute(query)
        

    def create_table_category(self,):

        query='create table category(id bigint primary key,school varchar(30),name varchar(30),summary varchar(1000),refer varchar(30))default charset utf8'

        self.execute(query)

    def check_str(self,string):
        return string.replace('\\','\\\\').replace('"','\\"')


    def insert_category(self,d):

        assert isinstance(d,dict),u'params d must be dict'

        ids=d['ids']
        school=d['school']
        name=d['name']
        refer=d['refer']
        summary=d['summary']

        summary=self.check_str(summary)


        query='''insert ignore into category(id,school,name,refer,summary) 
                values("%s","%s","%s","%s","%s")'''%(ids,school,name,refer,summary)
            

        self.execute(query)





