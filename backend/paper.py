'''
Author: flwfdd
Date: 2022-07-10 17:19:45
LastEditTime: 2022-07-28 10:49:21
Description: 文章模块
_(:з」∠)_
'''
import db
import user
import datetime
import reaction
from sqlalchemy import and_, func, or_
import config
from pymysql.converters import escape_string


# 上传或修改文章
def post(id, title, intro, data, last_time, now_time, anonymous, share):
    last_t = datetime.datetime.fromtimestamp(int(last_time))
    now_t = datetime.datetime.fromtimestamp(int(now_time))
    anonymous = bool(anonymous)
    share = bool(share)
    if id == '0':
        p = db.Paper(title=title, intro=intro, data=data, create_time=now_t,
                     update_time=now_t, user=user.now_uid, anonymous=anonymous, share=share, owner=user.now_uid)
        db.add(p)
        db.commit()
        id = p.id
    else:
        p = db.Paper.query.filter(
            and_(db.Paper.id == id, db.Paper.show == True)).first()
        if not (p.share or user.ifown(p.owner)):
            return -1
        if p.update_time > last_t:
            return 0
        p.title = title
        p.intro = intro
        p.data = data
        p.update_time = now_t
        p.user = user.now_uid
        p.anonymous = anonymous
        if user.ifown(p.owner):
            p.share = share
        db.commit()
    ph = db.PaperHistory(paper_id=id, title=title, intro=intro, data=data,
                         create_time=now_t, user=user.now_uid, anonymous=anonymous)
    db.add(ph)
    db.commit()
    return p.id


# 获取文章
def get(id):
    p = db.Paper.query.filter(
        and_(db.Paper.id == id, db.Paper.show == True)).first()
    dic = db.to_dict(p)
    dic['like'] = reaction.get_like_status('paper'+str(id))
    if dic['anonymous'] and dic['user'] != user.now_uid:
        dic['user'] = '-1'
    dic['user'] = user.get_info(dic['user'])
    dic['own'] = user.ifown(dic['owner'])
    dic['owner'] = ''
    return dic


# 获取文章
def list(search, order, page):
    q = db.Paper.query.filter_by(show=True)
    if search:
        search=escape_string(search)
        q = q.filter(or_(db.Paper.title.like("%{}%".format(search)), db.Paper.intro.like(
            "%{}%".format(search)), db.Paper.data.like("%{}%".format(search))))
    elif order=='like':
        q=q.order_by(db.Paper.like_num.desc(),db.Paper.update_time.desc())
    elif order=='new':
        q=q.order_by(db.Paper.update_time.desc())
    else:
        q=q.order_by(func.rand())
    q=q.offset(int(page)*config.page_size).limit(config.page_size).all()
    out=[]
    for i in q:
        out.append({
            'id':i.id,
            'title':i.title,
            'intro':i.intro,
            'like_num':i.like_num,
            'comment_num':i.comment_num,
            'update_time':i.update_time,
        })
    return out
