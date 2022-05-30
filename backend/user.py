'''
Author: flwfdd
Date: 2022-03-08 21:31:25
LastEditTime: 2022-05-30 15:10:07
Description: 用户管理
_(:з」∠)_
'''
from urllib import request
import uuid
import redis
from functools import wraps
from flask import request, abort
from werkzeug.local import LocalProxy
import random

import config
import webvpn
import db
import mail

red = redis.StrictRedis(host=config.redis_host,
                        port=config.redis_port, decode_responses=True)

now_uid = LocalProxy(lambda: request.uid)


# 检查登陆状态装饰器
def check(strict=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            flag = 1
            cookie = request.headers.get('Fake-Cookie', '')
            if not cookie:
                flag = 0
            uid = red.get(cookie)
            if not uid:
                flag = 0
            if not flag:
                if strict:
                    abort(401)
                else:
                    request.uid = 0
            else:
                request.uid = uid
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 发送邮箱验证码
def mail_verify(sid):
    verify_code = str(random.randint(0, 999999)).zfill(6)
    red.set('verify'+sid, verify_code, 600)
    if mail.send(sid+'@bit.edu.cn', '[BITself]验证码', '【{}】 是你的验证码ヾ(^▽^*)))'.format(verify_code)):
        return True
    else:
        return False


# 注册
def register(sid, password, verify_code):
    if red.get('verify'+sid) != verify_code:
        return False
    q = db.User.query.filter_by(sid=sid).first()
    if not q:
        qq = True
        while qq:
            nickname = 'BITself'+str(uuid.uuid4())[:8]
            qq = db.User.query.filter_by(nickname=nickname).first()
        u = db.User(sid=sid, password=password, nickname=nickname)
        db.add(u)
        db.commit()
        q = db.User.query.filter_by(sid=sid).first()
    else:
        q.password = password
        db.commit()
    cookie = str(uuid.uuid4())
    red.set(cookie, q.sid, ex=config.ex_time)
    return cookie


# 登录
def login(sid, password):
    q = db.User.query.filter_by(sid=sid).first()
    if q and q.password==password:
        cookie = str(uuid.uuid4())
        red.set(cookie, q.id, ex=config.ex_time)
        return cookie
    return False


# 账号密码登录
# def login(username, password, execution, cookie, remember):
#     uid = webvpn.login(username, password, execution, cookie)
#     if uid:
#         cookie = str(uuid.uuid4())
#         red.set(cookie, uid, ex=config.ex_time)
#         return cookie
#     return False


# 获取用户信息
def my_info():
    q = db.User.query.filter_by(id=now_uid).first()
    return db.to_json(q)


# 修改信息
def edit_info(nickname, motto, avatar):
    u = db.User.query.get(now_uid)
    if nickname:
        u.nickname = nickname
    if motto:
        u.motto = motto
    if avatar:
        u.avatar = avatar
    db.commit()
