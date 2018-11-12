# _*_ coding:utf-8 _*_ 

from cookies import load_cookies


import os

path='lession'

print os.path.exists(path)
os.mkdir(path)

print os.path.exists(path)
