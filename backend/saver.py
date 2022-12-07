'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-11-11 11:18:40
Description: 图床模块
_(:з」∠)_
'''
from PIL import Image
from io import BytesIO
import os
import hashlib
import requests
import time

import db
import user
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

cos_config = CosConfig(Region=config.cos_region,
                       SecretId=config.cos_secret_id, SecretKey=config.cos_secret_key)
cos_client = CosS3Client(cos_config)


def init():
    if not os.path.exists(os.path.join(config.save_path, 'img')):
        os.makedirs(os.path.join(config.save_path, 'img'))


# 保存文件 path如img/233.jpg
def save(path, data, cos=False, onedrive=False):
    with open(os.path.join(config.save_path, path), "wb") as f:
        f.write(data)
    if cos:
        cos_client.put_object(
            Bucket=config.cos_bucket,
            Body=data,
            Key=os.path.join(config.cos_path, path)
        )
    if onedrive:
        onedrive_upload_file(path, data)


# 上传图片 返回链接
def upload_img(data, name):
    img = Image.open(BytesIO(data))
    id = hashlib.md5(data).hexdigest()+'.'+img.format.lower()
    q = db.Image.query.filter_by(id=id).first()
    if not q:
        img = db.Image(id=id, size=len(data), name=name, user=user.now_uid)
        db.add(img)
        save('img/'+id, data, cos=True)
    db.commit()
    return img_url(id)


# 将图片id转为url
def img_url(id):
    if not id:
        id = "e2e4437695e019484769bc807948dad8.jpeg"
    return os.path.join(config.save_url, "img", id)


# 图片url转id
def img_id(url):
    return os.path.basename(url)


# 通过链接上传图片 返回链接
def upload_img_by_url(url):
    r = requests.get(url)
    return upload_img(r.content, url)


# Onedrive 模块
onedrive_refresh_time = 0
onedrive_token = ""


def onedrive_get_head():
    global onedrive_refresh_time, onedrive_token
    if time.time() > onedrive_refresh_time:
        data = {
            'client_id': config.onedrive_client_id,
            'client_secret': config.onedrive_client_secret,
            'redirect_uri': 'http://localhost',
            'refresh_token': config.onedrive_refresh_token,
            'grant_type': 'refresh_token'
        }
        dic = requests.post(config.onedrive_auth_api, data=data).json()
        onedrive_refresh_time = time.time()+dic['expires_in']-11
        onedrive_token = 'bearer '+dic['access_token']
    return {
        'Authorization': onedrive_token,
    }


def onedrive_get_path(path, op):
    if path[0] == '/':
        path = path[1:]
    if path[-1] == '/':
        path = path[:-1]
    if op[0] == '/':
        op = op[1:]
    return config.onedrive_api+'/root:/BIT101/{}:/{}'.format(path, op)


def onedrive_upload_url(path,conflict="fail"):
    data = {
        "item": {
            "@microsoft.graph.conflictBehavior": conflict
        }
    }
    r=requests.post(onedrive_get_path(
        path, 'createUploadSession'), headers=onedrive_get_head(), json=data)
    if r.status_code==200:
        return r.json()['uploadUrl']
    else: return ""


def onedrive_upload_file(path, data):
    size = len(data)
    if size > 4000000:
        url = onedrive_upload_url(path)
        chunk_size = 3276800
        for i in range(0, size, chunk_size):
            chunk_data = data[i:i+chunk_size]
            r = requests.put(url, headers={'Content-Length': str(len(chunk_data)),
                             'Content-Range': 'bytes {}-{}/{}'.format(i, i+len(chunk_data)-1, size)}, data=chunk_data)
            if r.status_code != 202:
                break
    else:
        r = requests.put(onedrive_get_path(path, 'content'),
                         headers=onedrive_get_head(), data=data)
    if r.status_code == 200 or r.status_code == 201:
        return True
    else:
        return False
