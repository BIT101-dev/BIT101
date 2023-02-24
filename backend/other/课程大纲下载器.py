'''
Author: flwfdd
Date: 2022-08-12 19:19:53
LastEditTime: 2023-02-24 22:09:19
Description: 
_(:з」∠)_
'''
import csv
import os
import requests


# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
def typeList():
    return {
        '255044462d312e350d0a':'pdf',
        '504b0304140006000800':'docx',
        }
 
 
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()
 
 
def get_filetype(data):
    if(len(data)<2048): return None
    bins = data[:20] #提取20个字符
    bins = bytes2hex(bins) #转码
    bins = bins.lower()#小写
    tl = typeList()  #文件类型
    ftype='doc'
    for hcode in tl.keys():
        lens = len(hcode) # 需要的长度
        if bins[0:lens] == hcode:
            ftype = tl[hcode]
            break
    if ftype == 'doc':#全码未找到，优化处理，码表取5位验证
        bins = bins[0:5]
        for hcode in tl.keys():
            if len(hcode) > 5 and bins == hcode[0:5]:
                ftype = tl[hcode]
                break
    return ftype

f=open("./2022-2023-1.csv","r",encoding='utf-8')
dic=csv.DictReader(f)

if not os.path.exists("./课程大纲"):
    os.mkdir("./课程大纲")

head = {'Cookie': ""}
url="http://jwms.bit.edu.cn/jsxsd/pyfa/pyfazd_xzjxdg?kch={}"
# url="https://webvpn.bit.edu.cn/http/77726476706e69737468656265737421fae04c8f69326144300d8db9d6562d/jsxsd/pyfa/pyfazd_xzjxdg?kch={}"
for i in dic:
    name="{}-{}".format(i['课程名'].replace("/","_"),i['课程号'])
    flag=False
    for filetype in ['pdf','doc','docx','html']:
        path="./课程大纲/{}/{}.{}".format(name,name,filetype)
        if os.path.exists(path): flag=True
    if flag: continue

    r=requests.get(url.format(i['课程号']),headers=head)
    filetype=get_filetype(r.content)
    if not filetype: continue
    print(i['课程名'],filetype)
    if not os.path.exists("./课程大纲/{}/".format(name)): os.mkdir("./课程大纲/{}/".format(name))
    path="./课程大纲/{}/{}.{}".format(name,name,filetype)
    with open(path,"wb") as f:
        f.write(r.content)
    
