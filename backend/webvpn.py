'''
Author: flwfdd
Date: 2022-03-09 14:52:20
LastEditTime: 2022-05-31 20:46:39
Description: webvpn相关服务 尽量解耦方便移植
_(:з」∠)_
'''
import requests
import json
from bs4 import BeautifulSoup as bs
import db
import re
import time

base_url = "https://webvpn.bit.edu.cn"
login_url = base_url + \
    "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue"
need_captcha_url=base_url + \
    "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/checkNeedCaptcha.htl"
get_captcha_url=base_url + \
    "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/getCaptcha.htl"
account_info_url = base_url + \
    "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login"
student_info_init_url = base_url + \
    "/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=4585275700341858&appName=jbxxapp"
student_info_url = base_url + \
    "/http/77726476706e69737468656265737421e3e354d225397c1e7b0c9ce29b5b/xsfw/sys/jbxxapp/modules/infoStudent/getStuBatchInfo.do"
score_base_url = base_url + \
    "/https/77726476706e69737468656265737421fae04c8f69326144300d8db9d6562d"
score_url = score_base_url+"/jsxsd/kscj/cjcx_list"


# 处理重定向问题
def redirection(url, head={}, data={}):
    r = requests.post(url, data, headers=head, allow_redirects=False)
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


# 查询是否需要验证码
def need_captcha(sid):
    r=redirection(need_captcha_url+"?username="+sid)
    return json.loads(r.text)['isNeed']


# 获取验证码
def get_captcha(cookie):
    r=redirection(get_captcha_url,head={'Cookie':cookie})
    return r.content

# 登录
def login(username, password, execution, cookie,captcha=""):
    head = {"Cookie": cookie}
    data = {
        'username': username,
        'password': password,
        'execution': execution,
        'captcha': captcha,
        '_eventId': "submit",
        'cllt': "userNameLogin",
        'dllt': "generalLogin",
        'lt': "",
        'rememberMe': "true",
    }
    # print(head, data)
    r = redirection(login_url, data=data, head=head)
    if r.status_code != 200 or "帐号登录或动态码登录" in r.text:
        return False
    return True


# 获取统一身份认证账号信息
def get_account_info(head):
    try:
        r = redirection(account_info_url, head=head)
        soup = bs(r.text, 'html.parser')
        l = soup.find(class_="dl-narrow dl-horizontal").findAll("dd")
        try:
            birthday = re.search("\[\d+\]", r.text).group()[7:15]
        except:
            birthday = ""
        info = {
            'name': l[1].text,
            'account_type': l[2].text,
            'birthday': birthday
        }
        return info
    except:
        return {}


# 获取学生基础信息
def get_student_info(username, head):
    try:
        redirection(student_info_init_url, head=head)
        r = redirection(student_info_url, head=head, data={
                        'requestParamStr': '{"XSBH":"%s"}' % username})
        dic = json.loads(r.text)['data']
        info = {
            'name': dic['XM'],
            'class_name': dic['BJDM_DISPLAY'],
            'sex': dic['XBDM_DISPLAY'],
            'college': dic['DWDM_DISPLAY'],
            'major':dic['ZYDM_DISPLAY']
        }
        return info
    except:
        return {}


# 获取成绩
def get_score(cookie, detail=False):
    head = {'Cookie': cookie}
    r = redirection(score_url, head=head)
    r = redirection(score_url, head=head)

    table_dic = []
    table_head = []
    if r.status_code == 200:
        if "统一身份认证" in r.text:
            return False
        soup = bs(r.text, 'html.parser')
        dataList = soup.find(id="dataList").find_all("tr")
        # 获取表头
        for i in dataList[0].find_all("th"):
            table_head.append(i.string)
        # 获取表体
        for row in dataList[1:]:
            dic = {}
            for ind, i in enumerate(row.find_all("td")):
                dic[table_head[ind]] = i.string if i.string else ""

            # 获取详情
            re_result = re.search(r"/jsxsd/kscj/cjfx.+cjfs", str(row))
            if detail and re_result:
                detail_url = re_result.group().replace("&amp;", "&")
                if detail_url:
                    r = redirection(score_base_url+detail_url,
                                    head={'Cookie': cookie})
                    soup = bs(r.text, 'html.parser')
                    for i in soup.find_all("td"):
                        if "：" in i.string:
                            ll = i.string.split("：")
                            dic[ll[0]] = ll[1]
            table_dic.append(dic)
    # 从字典转为表格格式
    table_head = {}
    table = [[]]
    for row in table_dic:
        table.append(['']*len(table_head))
        for i in row:
            if i not in table_head:
                table_head[i] = len(table_head)
                table[0].append(i)
            ind = table_head[i]
            table[-1] += ['']*(ind-len(table[-1])+1)
            table[-1][ind] = row[i]
    return table
