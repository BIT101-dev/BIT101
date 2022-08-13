'''
Author: flwfdd
Date: 2022-08-12 19:19:53
LastEditTime: 2022-08-12 19:44:59
Description: 
_(:з」∠)_
'''
import csv
import os
import requests

f=open("./2020-2021-1.csv","r",encoding='utf-8')
dic=csv.DictReader(f)

if not os.path.exists("./课程大纲"):
    os.mkdir("./课程大纲")

head = {'Cookie': "wengine_vpn_ticketwebvpn_bit_edu_cn=6fa50adc1d9836f4;"}
url="https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421fae04c8f69326144300d8db9d6562d/jsxsd/pyfa/pyfazd_xzjxdg?kch={}"
for i in dic:
    path="./课程大纲/{}-{}.doc".format(i['课程名'].replace("/","_"),i['课程号'])
    if os.path.exists(path): continue
    r=requests.get(url.format(i['课程号']),headers=head)
    with open(path,"wb") as f:
        f.write(r.content)
    
