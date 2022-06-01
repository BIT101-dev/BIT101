'''
Author: flwfdd
Date: 2022-03-08 21:31:25
LastEditTime: 2022-06-01 19:30:25
Description: 用户管理
_(:з」∠)_
'''
import base64
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
import saver

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


# 统一身份认证验证初始化
def webvpn_verify_init(sid):
    dic=webvpn.init_login()
    if webvpn.need_captcha(sid):
        img=webvpn.get_captcha(dic['cookie'])
        dic['captcha']=base64.b64encode(img).decode()
    else:
        dic['captcha']=False
    return dic
    
    

# 统一身份认证
def webvpn_verify(username, password, execution, cookie,captcha=""):
    if webvpn.login(username, password, execution, cookie,captcha):
        verify_code = str(random.randint(0, 999999)).zfill(6)
        red.set('verify'+username, verify_code, 600)
        return verify_code
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
    red.set(cookie, q.id, ex=config.ex_time)
    return cookie


# 登录
def login(sid, password):
    q = db.User.query.filter_by(sid=sid).first()
    if q and q.password==password:
        cookie = str(uuid.uuid4())
        red.set(cookie, q.id, ex=config.ex_time)
        return cookie
    return False


# 获取用户信息
def get_info(uid):
    if uid=='0':
        if not now_uid: abort(401)
        uid=now_uid
    q = db.User.query.filter_by(id=uid).first()
    q.password=""
    q.avatar=saver.img_url(q.avatar)
    return db.to_dict(q)


# 修改信息
def edit_info(nickname, motto, avatar):
    u = db.User.query.get(now_uid)
    u.nickname = nickname
    u.motto = motto
    u.avatar = saver.img_id(avatar)
    try:
        db.commit()
        return True
    except:
        return False
