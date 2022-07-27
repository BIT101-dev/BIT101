'''
Author: flwfdd
Date: 2022-07-14 19:57:35
LastEditTime: 2022-07-26 21:29:58
Description: 用户交互部分 如点赞评论
_(:з」∠)_
'''
import user
import db
import config
from sqlalchemy import and_


# 获取操作对象
def get_obj(obj):
    if obj[:5] == 'paper':
        return db.Paper.query.filter_by(id=obj[5:]).first()
    if obj[:7] == 'comment':
        return db.Comment.query.filter_by(id=obj[7:]).first()


# 获取当前用户点赞状态
def get_like_status(obj):
    q = db.Like.query.filter(and_(
        db.Like.user == user.now_uid, db.Like.obj == obj, db.Like.show == True)).first()
    return bool(q)


# 点赞
def post_like(obj):
    uid = user.now_uid
    q = db.Like.query.filter(
        and_(db.Like.user == uid, db.Like.obj == obj)).first()
    o = get_obj(obj)
    if q and q.show:
        o.like_num -= 1
        q.show = False
    else:
        o.like_num += 1
        if q:
            q.show = True
        else:
            q = db.Like(user=uid, obj=obj)
            db.add(q)
    db.commit()
    return {'like': q.show, 'like_num': o.like_num}


def package_comment(i):
    i['own'] = user.ifown(i['user'])
    if i['anonymous']:
        i['user'] = -1
    i['user'] = user.get_info(i['user'])
    i['sub'] = []
    i['like']=get_like_status('comment'+str(i['id']))
    if i['reply_user'] != 0:
        i['reply_user'] = user.get_info(i['reply_user'])
    if i['comment_num']:
        i['sub'] = get_comments('comment'+str(i['id']), 'default', 0)

# 获取评论
def get_comments(obj, order, page):
    q = db.Comment.query.filter(
        and_(db.Comment.obj == obj, db.Comment.show == True))
    if order == 'old':
        q = q.order_by(db.Comment.create_time)
    elif order == 'new':
        q = q.order_by(db.Comment.create_time.desc())
    else:
        q = q.order_by(db.Comment.update_time.desc())
    q = q.offset(int(page)*config.page_size).limit(config.page_size).all()
    out =db.to_dict(q)
    for i in out:
       package_comment(i)
    return out


# 评论
def post_comment(obj, text, anonymous, reply_user='0',rate='0'):
    anonymous=bool(anonymous)
    rate=int(rate)
    q = db.Comment(user=user.now_uid, obj=obj, text=text,
                   anonymous=anonymous, reply_user=reply_user)
    db.add(q)
    o = get_obj(obj)
    o.comment_num += 1
    if rate:
        o.rate_num+=1
        o.rate_sum+=rate
    db.commit()
    i = db.to_dict(q)
    package_comment(i)
    return i

# 删除评论
def delete_comment(id):
    q=db.Comment.query.filter_by(id=id).first()
    q.show=False
    o=get_obj(q.obj)
    o.comment_num-=1
    if q.rate:
        o.rate_num-=1
        o.rate_sum-=q.rate
    db.commit()