'''
Author: flwfdd
Date: 2022-07-14 19:57:35
LastEditTime: 2022-07-14 21:24:41
Description: 用户交互部分 如点赞评论
_(:з」∠)_
'''
import user
import db
from sqlalchemy import and_


# 获取点赞对象
def get_obj(obj):
    if obj[:5] == 'paper':
        return db.Paper.query.filter_by(id=obj[5:]).first()


# 获取点赞状态
def get_like_status(obj):
    q = db.Like.query.filter(and_(
        db.Like.user_id == user.now_uid, db.Like.obj == obj, db.Like.show == True)).first()
    return bool(q)


# 点赞
def post_like(obj):
    uid = user.now_uid
    q = db.Like.query.filter(
        and_(db.Like.user_id == uid, db.Like.obj == obj)).first()
    o = get_obj(obj)
    if q and q.show:
        o.like_num -= 1
        q.show = False
    else:
        o.like_num += 1
        if q:
            q.show = True
        else:
            q = db.Like(user_id=uid, obj=obj)
            db.add(q)
    db.commit()
    return {'like': q.show, 'like_num': o.like_num}
