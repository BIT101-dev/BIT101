'''
Author: flwfdd
Date: 2022-03-08 21:26:58
LastEditTime: 2022-06-01 18:09:03
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
import saver
import course

app = Flask(__name__)
CORS(app, resources=r"/*")
app.config['MAX_CONTENT_LENGTH'] = config.max_upload_size

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


# 返回
def res(data, status=200):
    return Response(json.dumps(data), status=status, mimetype='application/json')


# 路由
@app.route("/")
@user.check()
def say_hello():
    return "Hello BITself!<br/>id:{}<br/>name:{}".format(request.headers.get('Fake-Cookie'), user.now_uid)


# 用户系统-----------------------------------------------------------------------------

# 获取邮件验证码
@app.route("/user/mail_verify/", methods=['GET'])
def user_mail_verify():
    sid = request.args.get('sid', '')
    if not sid:
        return res({'msg': '请检查请求参数awa'}, 400)
    if user.mail_verify(sid):
        return {'msg': '发送成功OvO有效期10分钟'}
    else:
        return res({'msg': '出错了Orz请重试或更换验证方式'}, 500)


# 统一身份认证初始化
@app.route("/user/webvpn_verify_init/")
def user_webvpn_verify_init():
    sid = request.args.get('sid', '')
    return user.webvpn_verify_init(sid)


# webvpn验证
@app.route("/user/webvpn_verify/", methods=['POST'])
def user_webvpn_verify():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    execution = data.get('execution', '')
    cookie = data.get('cookie', '')
    captcha = data.get('captcha', '')
    if not (username and password and execution and cookie):
        return res({'msg': '请检查请求参数awa'}, 400)
    verify_code = user.webvpn_verify(
        username, password, execution, cookie, captcha)
    if verify_code:
        return {'verify_code': verify_code, 'msg': '验证通过啦'}
    else:
        return res({'msg': '验证失败Orz'}, 500)


# 注册
@app.route("/user/register/", methods=['GET'])
def user_register():
    sid = request.args.get('sid', '')
    password = request.args.get('password', '')
    verify_code = request.args.get('verify_code', '')
    if not (sid and password and verify_code):
        return res({'msg': '请检查请求参数awa'}, 400)
    cookie = user.register(sid, password, verify_code)
    if cookie:
        return {'msg': '注册成功OvO', 'fake_cookie': cookie}
    return res({'msg': '注册失败Orz'}, 500)


# 登录
@app.route("/user/login/", methods=['GET'])
def user_login():
    sid = request.args.get('sid', '')
    password = request.args.get('password', '')
    if not (sid and password):
        return res({'msg': '请检查请求参数awa'}, 400)
    cookie = user.login(sid, password)
    if cookie:
        return {'msg': '登陆成功OvO', 'fake_cookie': cookie}
    return res({'msg': '登录失败Orz'}, 500)


# 获取用户信息
@app.route("/user/info/", methods=['GET'])
@user.check(False)
def user_get_info():
    uid = request.args.get('id', '0')
    return user.get_info(uid)


# 修改个人信息
@app.route("/user/info/", methods=['PUT'])
@user.check()
def user_edit_info():
    data = request.get_json()
    nickname = data.get('nickname', '')
    motto = data.get('motto', '')
    avatar = data.get('avatar', '')
    if not (nickname and motto and avatar):
        return res({'msg': '请检查请求参数awa'}, 400)
    if user.edit_info(nickname=nickname, motto=motto, avatar=avatar):
        return {'msg':'修改成功OvO'}
    else:
        return res({'msg': '修改失败Orz可能是昵称太长或重复'}, 500)


# 查询成绩
@app.route("/get_score/")
@user.check()
def get_score():
    cookie = request.args.get('cookie', '')
    out = webvpn.get_score(cookie)
    if out:
        return Response(json.dumps(out),  mimetype='application/json')
    else:
        abort(424)


# 查询成绩细节
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


# 图片上传
@app.route('/upload/image/', methods=["POST"])
@user.check()
def upload_image():
    file=request.files.get('file','')
    if not file: abort(500)
    url = saver.upload_img(file)
    return {'url':url}


# 获取单个课程
@app.route("/course/detail/")
def course_detail():
    id = request.args.get('id', '')
    return course.detail(id)


# 评教
@app.route("/course/rate/")
@user.check()
def course_rate():
    id = request.args.get('id', '')
    rating = request.args.get('rating', '')
    comment = request.args.get('comment', '')
    anonymous = request.args.get('anonymous', '0')
    return course.rate(id, rating, comment, anonymous)


# 评教列表
@app.route("/course/rate_list/")
@user.check(False)
def course_rate_list():
    id = request.args.get('id', '')
    page = request.args.get('page', '0')
    out = course.rate_list(id, int(page))
    return Response(json.dumps(out),  mimetype='application/json')


# 评教点赞
@app.route("/course/rate_like/")
@user.check()
def course_rate_like():
    id = request.args.get('id', '')
    like = request.args.get('like', '0')
    return course.rate_like(id, bool(int(like)))


# 搜索课程
@app.route("/course/search/")
def course_search():
    course_search = request.args.get('course_search', '')
    teacher_search = request.args.get('teacher_search', '')
    page = request.args.get('page', '0')
    out = course.search(course_search, teacher_search, int(page))
    return Response(json.dumps(out),  mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
