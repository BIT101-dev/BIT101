'''
Author: flwfdd
Date: 2022-03-08 21:26:58
LastEditTime: 2022-08-14 01:31:14
Description: 主程序
_(:з」∠)_
'''
from datetime import datetime, date
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
import paper
import reaction
import variable

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
    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)
    return Response(json.dumps(data, cls=ComplexEncoder), status=status, mimetype='application/json')


# 路由
@app.route("/")
@user.check()
def say_hello():
    return "Hello BIT101!<br/>id:{}<br/>name:{}".format(request.headers.get('Fake-Cookie'), user.now_uid)


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
        return {'verify_code': verify_code, 'cookie': cookie, 'msg': '验证通过啦'}
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
    return res(user.get_info(uid), 200)


# 修改个人信息
@app.route("/user/info/", methods=['POST'])
@user.check()
def user_edit_info():
    data = request.get_json()
    nickname = data.get('nickname', '')
    motto = data.get('motto', '')
    avatar = data.get('avatar', '')
    if not (nickname and motto and avatar):
        return res({'msg': '请检查请求参数awa'}, 400)
    if user.edit_info(nickname=nickname, motto=motto, avatar=avatar):
        return {'msg': '修改成功OvO'}
    else:
        return res({'msg': '修改失败Orz可能是昵称太长或重复'}, 500)


# 图片上传
@app.route('/upload/image/', methods=["POST"])
@user.check()
def upload_image():
    file = request.files.get('file', '')
    if file:
        url = saver.upload_img(file.read(), file.filename)
    else:
        ori_url = request.get_json().get('url', '')
        if ori_url:
            url = saver.upload_img_by_url(ori_url)
        else:
            abort(500)
    return {'url': url}


# 查询成绩
@app.route("/score/", methods=['GET'])
@requests_proxy()
def get_score_brief():
    cookie = request.args.get('cookie', '')
    detail = request.args.get('detail', False)
    out = webvpn.get_score(cookie, detail=detail)
    if out:
        return res({'data': out, 'msg': '查询成功OvO'}, 200)
    else:
        return res({'msg': '未通过统一身份认证Orz'}, 500)


# 获取成绩单
@app.route("/score/report/", methods=['GET'])
def get_score_report():
    cookie = request.args.get('cookie', '')
    out = webvpn.get_report(cookie)
    if out:
        return res({'data': out, 'msg': '查询成功OvO'}, 200)
    else:
        return res({'msg': '未通过统一身份认证Orz'}, 500)


# 获取文章
@app.route("/paper/", methods=['GET'])
@user.check(False)
def get_paper():
    id = request.args.get('id')
    if not id:
        return res({'msg': '请检查请求参数awa'}, 400)
    return res(paper.get(id), 200)


# 上传文章
@app.route("/paper/", methods=['POST'])
@user.check()
def post_paper():
    dic = request.get_json()
    id = dic.get('id')
    title = dic.get('title')
    intro = dic.get('intro', '')
    data = dic.get('data')
    last_time = dic.get('last_time', '0')
    now_time = dic.get('now_time')
    anonymous = dic.get('anonymous', False)
    share = dic.get('share', True)
    if not (id and title and data and now_time and now_time):
        return res({'msg': '请检查请求参数awa'}, 400)
    id = paper.post(id, title, intro, data, last_time,
                    now_time, anonymous, share)
    if id > 0:
        return res({'msg': '发表成功OvO', 'id': id}, 200)
    elif id == 0:
        return res({'msg': '请基于文章最新版本编辑~'}, 500)
    else:
        return res({'msg': '没有编辑权限'}, 500)


# 获取文章列表
@app.route("/papers/", methods=['GET'])
def get_papers():
    search = request.args.get('search', '')
    order = request.args.get('order', 'default')
    page = request.args.get('page', '0')
    return res(paper.list(search, order, page), 200)


# 点赞
@app.route("/reaction/like/", methods=['POST'])
@user.check()
def post_reaction_like():
    dic = request.get_json()
    obj = dic.get('obj')
    if not obj:
        return res({'msg': '请检查请求参数awa'}, 400)
    return reaction.post_like(obj)


# 获取评论
@app.route("/reaction/comments/", methods=['GET'])
@user.check(False)
def get_reaction_comments():
    obj = request.args.get('obj')
    order = request.args.get('order', 'default')
    page = request.args.get('page', '0')
    if not (obj and page.isdigit()):
        return res({'msg': '请检查请求参数awa'}, 400)
    dic = reaction.get_comments(obj, order, page)
    return res(dic, 200)


# 评论
@app.route("/reaction/comment/", methods=['POST'])
@user.check()
def post_reaction_comment():
    dic = request.get_json()
    obj = dic.get('obj')
    anonymous = dic.get('anonymous', False)
    text = dic.get('text')
    reply_user = str(dic.get('reply_user', ''))
    if not reply_user:
        reply_user = '0'
    rate = str(dic.get('rate', '0'))
    if not (obj and text and reply_user and rate):
        return res({'msg': '请检查请求参数awa'}, 400)
    dic = reaction.post_comment(obj, text, anonymous, reply_user, rate)
    if dic:
        dic['msg'] = '评论成功OvO'
        return dic
    else:
        return res({'msg': '不能重复评价'}, 500)


# 删除评论
@app.route("/reaction/comment/", methods=['DELETE'])
@user.check()
def delete_reaction_comment():
    id = request.args.get('id', '')
    if not reaction.delete_comment(id):
        return res({'msg': '请检查请求参数awa'}, 400)
    return res({'msg': '删除成功OvO'}, 200)


# 设置变量
@app.route("/variable/", methods=['POST'])
@user.check_admin()
def post_variable():
    dic = request.get_json()
    obj = dic.get('obj')
    data = dic.get('data')
    variable.post(obj, data)
    return res({'msg': "设置成功OvO"}, 200)


# 获取变量
@app.route("/variable/", methods=['GET'])
def get_variable():
    obj = request.args.get('obj', '')
    out = variable.get(obj)
    return out


# 获取单个课程
@app.route("/course/", methods=['GET'])
@user.check(False)
def get_course_detail():
    id = request.args.get('id', '')
    return res(course.detail(id), 200)


# 搜索课程
@app.route("/courses/", methods=['GET'])
def get_course_search():
    search = request.args.get('search', '')
    order = request.args.get('order', 'default')
    page = request.args.get('page', '0')
    out = course.list(search, order, page)
    return res(out,200)


# 获取课程资料上传链接
@app.route("/course/upload/url/", methods=['GET'])
@user.check()
def get_course_upload_url():
    number = request.args.get('number', '')
    tp = request.args.get('type', '')
    name = request.args.get('name', '')
    if not (number and tp and name):
        return res({''})
    out = course.upload_url(number, tp, name)
    if out: return res(out, 200)
    else: return res({'msg':'获取上传链接失败Orz可能是文件重复'},500)


# 课程资料上传记录
@app.route("/course/upload/log/", methods=['POST'])
@user.check()
def post_course_upload_log():
    dic = request.get_json()
    id = dic.get('id')
    msg = dic.get('msg','')
    if course.upload_log(id,msg):
        return res({'msg': "上传成功OvO"}, 200)
    else: return res({'msg':'上传记录失败Orz'},500)


if __name__ == '__main__':
    variable.init()
    saver.init()
    app.run(host="0.0.0.0", port=5000)
    
