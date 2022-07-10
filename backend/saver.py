'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-07-10 15:20:11
Description: 图床模块
_(:з」∠)_
'''
from PIL import Image
from io import BytesIO
import os
import hashlib
import requests

import db
import user
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

cos_config = CosConfig(Region=config.cos_region,
                       SecretId=config.cos_secret_id, SecretKey=config.cos_secret_key)
cos_client = CosS3Client(cos_config)

def init():
    if not os.path.exists(os.path.join(config.save_path,'img')):
        os.makedirs(os.path.join(config.save_path,'img'))

# 保存文件 path如img/233.jpg
def save(data, path, cos=False, onedrive=False):
    with open(os.path.join(config.save_path,path), "wb") as f:
        f.write(data)
    if cos:
        cos_client.put_object(
            Bucket=config.cos_bucket,
            Body=data,
            Key=os.path.join(config.cos_path,path)
        )
    if onedrive: pass


# 上传图片 返回链接
def upload_img(data, name):
    img = Image.open(BytesIO(data))
    id = hashlib.md5(data).hexdigest()+'.'+img.format.lower()
    q = db.Image.query.filter_by(id=id).first()
    if not q:
        img = db.Image(id=id, size=len(data), name=name, user=user.now_uid)
        db.add(img)
        save(data, 'img/'+id, cos=True)
    db.commit()
    return img_url(id)


# 将图片id转为url
def img_url(id):
    if not id:
        id = "e2e4437695e019484769bc807948dad8.jpeg"
    return os.path.join(config.save_url,"img",id)


# 图片url转id
def img_id(url):
    return os.path.basename(url)


# 通过链接上传图片 返回链接
def upload_img_by_url(url):
    r = requests.get(url)
    return upload_img(r.content, url)

init()