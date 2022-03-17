'''
Author: flwfdd
Date: 2022-03-08 21:31:25
LastEditTime: 2022-03-10 09:19:25
Description: 用户管理
_(:з」∠)_
'''
from urllib import request
import uuid
import redis
import config
import webvpn
import db
from functools import wraps
from flask import request, abort
from werkzeug.local import LocalProxy

red = redis.StrictRedis(host=config.redis_host,
                        port=config.redis_port, decode_responses=True)

now_uid = LocalProxy(lambda: request.uid)


# 检查登陆状态装饰器
def check():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cookie = request.headers.get('Fake-Cookie', '')
            if not cookie:
                abort(401)
            uid = red.get(cookie)
            if not uid:
                abort(401)
            request.uid = uid
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 账号密码登录
def login(username, password, execution, cookie, remember):
    uid=webvpn.login(username, password, execution, cookie)
    if uid:
        cookie = str(uuid.uuid4())
        red.set(cookie, uid, ex=config.ex_time)
        return cookie
    return False


# 获取用户信息
def my_info():
    q=db.User.query.filter_by(id=now_uid).first()
    return db.to_json(q)

# 修改信息
def edit_info(nickname,motto,avatar):
    u=db.User.query.get(now_uid)
    if nickname:u.nickname=nickname
    if motto:u.motto=motto
    if avatar:u.avatar=avatar
    db.commit()