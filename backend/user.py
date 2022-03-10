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
from functools import wraps
from flask import request, abort
from werkzeug.local import LocalProxy

red = redis.StrictRedis(host=config.redis_host,
                        port=config.redis_port, decode_responses=True)

now = LocalProxy(lambda: request.student_id)

# 检查登陆状态装饰器
def check():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            cookie=request.headers.get('Fake-Cookie','')
            if not cookie: abort(401)
            student_id=red.get(cookie)
            if not student_id: abort(401)
            request.student_id=student_id
            return f(*args,**kwargs)
        return decorated_function
    return decorator

# 账号密码登录
def login(username, password,execution,cookie, remember):
    if webvpn.login(username,password,execution,cookie):
        cookie = str(uuid.uuid4())
        red.set(cookie, username, ex=config.ex_time)
        return cookie
    return False
