#_*_ coding:utf-8 _*_

'''

模拟登陆，获取cookies
'''

import time
from selenium import webdriver

def login():
    '''selenium 模拟登陆'''

    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 更换头部
    options.add_argument('user-agent=Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1')
    driver = webdriver.Chrome(chrome_options=options)
    login_url = 'https://www.icourse163.org/'
    driver.get(login_url)
    time.sleep(2)
    login_text=u'登录'.encode('utf-8')
    login_class='f-f0 navLoginBtn'
    login_xpath='//*[@id="auto-id-1530860345260"]'
    login=driver.find_element_by_partial_link_text(login_text)

    login.click()
    print u'sleep 2 second wait frame load successfully'
    time.sleep(2)
    frame=driver.find_element_by_xpath('//*[@id="auto-id-1540203413007"]')
    driver.switch_to.frame(frame)


    email=driver.find_element_by_name('email')
    password=driver.find_element_by_name('password')
    print u'sleep 2 second wait load all source'
    time.sleep(2)

    email.send_keys('chinaylssly@163.com')
    password.send_keys('你的密码')
    button=driver.find_element_by_id('dologin')

    button.click()

    r=raw_input(u'if login success,please type any word:')
    cookies=driver.get_cookies()

    driver.quit()
    d={}
    for i in cookies:
        d[i['name']]=i['value']

    return d

    









if __name__ =='__main__':

    login()

    
    pass