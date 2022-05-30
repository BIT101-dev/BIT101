'''
Author: flwfdd
Date: 2022-03-08 21:26:58
LastEditTime: 2022-05-30 14:19:03
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
import image_bed
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


# 用户系统

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


# 登陆
# @app.route("/login/", methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data['username']
#     password = data['password']
#     execution = data['execution']
#     cookie = data['cookie']
#     remember = data.get('remember', False)
#     fake_cookie = user.login(username, password, execution, cookie, remember)
#     if fake_cookie:
#         res = make_response({"status": "ok"})
#         res.headers['fake_cookie'] = fake_cookie
#         res.headers['Access-Control-Expose-Headers'] = 'fake_cookie'
#         return res
#     else:
#         abort(401)


# 登陆准备
@app.route("/login/init/")
def login_init():
    return webvpn.init_login()


# 登陆准备
@app.route("/my/info/")
@user.check()
def my_info():
    return user.my_info()


# 修改个人信息
@app.route("/my/edit_info/")
@user.check()
def my_edit_info():
    nickname = request.args.get('nickname', '')
    motto = request.args.get('motto', '')
    avatar = request.args.get('avatar', '')
    user.edit_info(nickname=nickname, motto=motto, avatar=avatar)
    return ""


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


# 图片上传
@app.route('/upload_image/', methods=["POST"])
@user.check()
def upload_image():
    files = request.files.getlist('files')
    out = image_bed.upload(files)
    return Response(json.dumps(out),  mimetype='application/json')


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
