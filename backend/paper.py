'''
Author: flwfdd
Date: 2022-07-10 17:19:45
LastEditTime: 2022-07-10 22:13:08
Description: 文章模块
_(:з」∠)_
'''
import db
import user
import datetime


# 上传或修改文章
def post(id, title, intro, data, last_time, now_time, anonymous):
    last_t = datetime.datetime.fromtimestamp(int(last_time))
    now_t = datetime.datetime.fromtimestamp(int(now_time))
    anonymous =(anonymous == '1')
    if id == '0':
        p = db.Paper(title=title, intro=intro, data=data, create_time=now_t,
                     update_time=now_t, user=user.now_uid, anonymous=anonymous)
        db.add(p)
        db.flush()
        db.commit()
        id = p.id
    else:
        p = db.Paper.query.filter_by(id=id).first()
        print(p.update_time,last_t)
        if p.update_time > last_t:
            return False
        p.title=title
        p.intro=intro
        p.data=data
        p.update_time=now_t
        p.user=user.now_uid
        p.anonymous=anonymous
        db.commit()
    ph = db.PaperHistory(paper_id=id, title=title, intro=intro, data=data,
                         create_time=now_t, user=user.now_uid, anonymous=anonymous)
    db.add(ph)
    db.commit()
    return p.id


# 获取文章
def get(id):
    p = db.Paper.query.filter_by(id=id).first()
    dic=db.to_dict(p)
    if dic['anonymous']:
        dic['user']=-1
    return dic