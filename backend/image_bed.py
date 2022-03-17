from ctypes import sizeof
from PIL import Image
from io import BytesIO
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


def upload(files):
    out = []
    for file in files:
        data = file.read()
        name = file.filename
        img = Image.open(BytesIO(data))
        id = hashlib.md5(data).hexdigest()+'.'+img.format
        q = db.Image.query.filter_by(id=id).first()
        if not q:
            img = db.Image(id=id, size=len(data), name=name, user=user.now_uid)
            db.add(img)
            save(data, id)
        out.append(id)
    db.commit()
    return out
