# -*- coding: utf-8 -*-
import requests
import time
from threading import Timer
import datetime
from selenium import webdriver
import requests
import time
import json
import os

from mydb import  MyDB

URL_BBS_ADMIN="https://bbs.uestc.edu.cn"
username="username"
password="password"
SLEEP_TIME=60
mydb=None

from bs4 import BeautifulSoup
isCookieDie=True
sess = requests.Session()
cookies_dict=None

def getmd5(text):
    """计算字符串md5

    Args:
        text ([type]): [description]

    Returns:
        [type]: [description]
    """
    import hashlib
    md5=hashlib.md5(text.encode('utf-8')).hexdigest()
    return md5

def initDB():
    """初始化数据库
    """
    global mydb
    if os.path.exists('test.sqlite'):
        mydb=MyDB("test.sqlite")
    else:
        mydb=MyDB("test.sqlite")
        mydb.sql('''
        CREATE TABLE Quotes
        (ID INTEGER  PRIMARY KEY  AUTOINCREMENT,
        md5           TEXT    NOT NULL,
        Quote           TEXT    NOT NULL
        );''')

def save_quote(text):
    """保存河畔的名言警句到本地数据库

    Args:
        text ([type]): [description]
    """
    print(text)
    a=mydb.select("Quotes","md5","md5='{}'".format(getmd5(text))).fetchall()
    if len(a)==0:
        mydb.insert("Quotes","md5,Quote",(getmd5(text),text))

def getCookies():
    """获取Cookie

    Returns:
        [type]: [description]
    """
    # 设置浏览器默认存储地址
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://bbs.uestc.edu.cn/member.php?mod=logging&action=login")
    # 输入用户名
    driver.find_element_by_name("username").send_keys(username)
    # 输入密码
    driver.find_element_by_name("password").send_keys(password)
    # 等待拖拽验证码
    
    # 点击提交
    driver.find_element_by_name("loginsubmit").click()
    time.sleep(5)
    # 获取cookie
    cookies = driver.get_cookies()
    driver.close()
    #print(type(cookies))
    #print(cookies)
        
    cookies_dict = dict()
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict



def crawler():
    """访问河畔
    """
    global isCookieDie
    global cookies_dict
    if isCookieDie:
        print("isCookieDie True")
        sess.headers.clear()# 将selenium的cookies放到session中
        cookies_dict=getCookies()
        isCookieDie=False
    print("isCookieDie False")
    url = URL_BBS_ADMIN
    html = sess.get(url,cookies=cookies_dict).text
    text= BeautifulSoup(html, 'html.parser').find('div',class_='vanfon_geyan').get_text().split('\n')[0]
    save_quote(text)
    if html.find('登录') != -1:
        isCookieDie=True

""" 
def set_timer():
    t = Timer(10, bbs_cookies)
    t.start() 
"""


if __name__ == '__main__':
    
    initDB() #初始化数据库
    while(1):
        crawler()
        time.sleep(SLEEP_TIME)
