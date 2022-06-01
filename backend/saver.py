'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-06-01 17:49:04
Description: 图床模块
_(:з」∠)_
'''
from PIL import Image
from io import BytesIO
import os
import hashlib
import db
import user
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

cos_config = CosConfig(Region=config.cos_region,
                       SecretId=config.cos_secret_id, SecretKey=config.cos_secret_key)
cos_client = CosS3Client(cos_config)


def save(data, name):
    with open(config.img_path+name, "wb") as f:
        f.write(data)
    cos_client.put_object(
        Bucket=config.cos_bucket,
        Body=data,
        Key=config.cos_path+name
    )


# 上传图片 返回链接
def upload_img(file):
    data = file.read()
    name = file.filename
    img = Image.open(BytesIO(data))
    id = hashlib.md5(data).hexdigest()+'.'+img.format.lower()
    q = db.Image.query.filter_by(id=id).first()
    if not q:
        img = db.Image(id=id, size=len(data), name=name, user=user.now_uid)
        db.add(img)
        save(data, id)
    db.commit()
    return img_url(id)


# 将图片id转为url
def img_url(id):
    if not id: id="f348659dddbb88f54a4185c1cfcae850.jpeg"
    return config.img_url+id

def img_id(url):
    return os.path.basename(url)