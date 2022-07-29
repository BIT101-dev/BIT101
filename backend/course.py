'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-07-29 23:03:51
Description: 
_(:з」∠)_
'''
import db
import config
from sqlalchemy import or_
import reaction


# 单个课程详情
def detail(id):
    course = db.Course.query.filter_by(id=id).first()
    dic=db.to_dict(course)
    dic['like']=reaction.get_like_status('course'+str(dic['id']))
    return dic


# 课程列表
def list(search,order, page):
    page=int(page)
    q = db.Course.query
    if search:
        q=q.filter(
        or_(db.Course.name.like("%{}%".format(search)),
            db.Course.number.like("%{}%".format(search)),
            db.Course.teachers_name.like("%{}%".format(search)),
            db.Course.teachers_number.like("%{}%".format(search)),))

    if order=='like': q=q.order_by(db.Course.like_num.desc())
    elif order=='comment': q=q.order_by(db.Course.comment_num.desc())
    elif order=='rate': q=q.order_by(db.Course.rate.desc())
    else: q=q.order_by(db.Course.update_time.desc())

    q=q.offset(page*config.page_size).limit(config.page_size).all()
    return db.to_dict(q)
