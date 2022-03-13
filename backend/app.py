'''
Author: flwfdd
Date: 2022-03-08 21:26:58
LastEditTime: 2022-03-10 09:16:26
Description: 主程序
_(:з」∠)_
'''
from flask import Flask, request, abort, make_response, Response
from flask_cors import CORS
from functools import wraps
import requests
import json
import user
import config
import db
import webvpn

app = Flask(__name__)
CORS(app, resources=r"/*")


# 数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.db.app = app
db.db.init_app(app)
db.db.create_all()


# 代理请求
def requests_proxy():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if config.requests_proxy:
                r = requests.get(config.requests_proxy+request.full_path)
                return r.content, r.status_code
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 路由
@app.route("/")
@user.check()
def say_hello():
    return "Hello BITself!<br/>id:{}<br/>name:{}".format(request.headers.get('Fake-Cookie'), user.now)


# 登陆
@app.route("/login/", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    execution = data['execution']
    cookie = data['cookie']
    remember = data.get('remember', False)
    fake_cookie = user.login(username, password, execution, cookie, remember)
    if fake_cookie:
        res = make_response({"status": "ok"})
        res.headers['fake_cookie'] = fake_cookie
        res.headers['Access-Control-Expose-Headers'] = 'fake_cookie'
        return res
    else:
        abort(401)


# 登陆准备
@app.route("/login/init/")
def login_init():
    return webvpn.init_login()


# 成绩查询
@app.route("/get_score/")
@user.check()
def get_score():
    cookie = request.args.get('cookie', '')
    out = webvpn.get_score(cookie)
    if out:
        return Response(json.dumps(out),  mimetype='application/json')
    else:
        abort(424)


# 成绩查询
@app.route("/get_score_detail/")
@user.check()
@requests_proxy()
def get_score_detail():
    cookie = request.args.get('cookie', '')
    out = webvpn.get_score(cookie, detail=True)
    if out:
        return Response(json.dumps(out),  mimetype='application/json')
    else:
        abort(424)


if __name__ == '__main__': 
    app.run(host="0.0.0.0", port=5000)
