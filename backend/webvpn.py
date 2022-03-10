'''
Author: flwfdd
Date: 2022-03-09 14:52:20
LastEditTime: 2022-03-10 00:21:54
Description: 
_(:з」∠)_
'''
import requests
import json
from bs4 import BeautifulSoup as bs
import db
import re

base_url = "https://webvpn.bit.edu.cn"
login_url = base_url + \
    "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue"
account_info_url=base_url+"/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login"
student_info_init_url=base_url+"/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=4585275700341858&appName=jbxxapp"
student_info_url=base_url+"/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/modules/infoStudent/getStuBatchInfo.do"


# 处理重定向问题
def redirection(url, head={},data={}):
    r=requests.post(url,data,headers=head,allow_redirects=False)
    while r.status_code == 302:
        url = r.headers['Location']
        if url[0] == '/':
            url = base_url+url
        # print(url)
        r = requests.get(url, headers=head, allow_redirects=False)
    return r

# 获取身份认证初始信息
def init_login():
    r = redirection(login_url)
    soup = bs(r.text, 'html.parser')
    x = soup.find(id="pwdFromId")
    salt = x.find(id="pwdEncryptSalt")['value']
    execution = x.find(id="execution")['value']
    cookie = r.headers['Set-Cookie']
    return {'salt': salt, 'execution': execution, 'cookie': cookie}

# 登录
def login(username, password, execution, cookie):
    head = {"Cookie": cookie}
    data = {
        'username': username,
        'password': password,
        'execution': execution,
        'captcha': "",
        '_eventId': "submit",
        'cllt': "userNameLogin",
        'dllt': "generalLogin",
        'lt': "",
        'rememberMe': "true",
    }
    # print(head, data)
    r=redirection(login_url,data=data,head=head)
    if r.status_code!=200 or "帐号登录或动态码登录" in r.text: return False
    if not db.User.query.filter_by(student_id=username).first():
        info=get_account_info(head)
        info.update(get_student_info(username,head))
        info['student_id']=username
        u=db.User()
        for i in info: u.__setattr__(i,info[i])
        db.add(u)
    return True

def get_account_info(head):
    try:
        r=redirection(account_info_url,head=head)
        soup=bs(r.text,'html.parser')
        l=soup.find(class_="dl-narrow dl-horizontal").findAll("dd")
        try:
            birthday=re.search("\[\d+\]",r.text).group()[7:15]
        except:
            birthday=""
        info={
            'name':l[1].text,
            'account_type':l[2].text,
            'birthday':birthday
            }
        return info
    except:
        return {}

def get_student_info(username,head):
    try:
        redirection(student_info_init_url,head=head)
        r=redirection(student_info_url,head=head,data={'requestParamStr':'{"XSBH":"%s"}'%username})
        dic=json.loads(r.text)['data']
        info={
            'name':dic['XM'],
            'class_name':dic['BJDM'],
            'sex':dic['XBDM_DISPLAY'],
            'college':dic['DWDM_DISPLAY']
        }
        return info
    except:
        return {}