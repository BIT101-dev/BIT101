'''
Author: flwfdd
Date: 2022-11-11 10:53:35
LastEditTime: 2022-11-11 11:24:46
Description: 用来获取 OneDrive 的 refresh_token 参考https://zhuanlan.zhihu.com/p/548194160
_(:з」∠)_
'''
import requests

code=""
url="https://login.microsoftonline.com/common/oauth2/v2.0/token"
client_id=""
client_secret=""

data={
    "client_id":client_id,
    "redirect_uri":"http://localhost",
    "client_secret":client_secret,
    "code":code,
    "grant_type":"authorization_code"
    }

r=requests.post(url,data=data)
try:
    print(r.json()['refresh_token'])
except:
    print(r.text)
