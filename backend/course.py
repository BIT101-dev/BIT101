'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-06-01 17:42:57
Description: 
_(:з」∠)_
'''
import db
import user
import config
from sqlalchemy import or_


# 单个课程详情
def detail(id):
    course = db.Course.query.filter_by(id=id).first()
    return db.to_dict(course)


# 评教
def rate(id, rating, comment, anonymous):
    uid = user.now_uid
    cr = db.CourseRate.query.filter(
        db.CourseRate.course_id == id, db.CourseRate.user_id == uid).first()
    c = db.Course.query.filter_by(id=id).first()
    rating = int(rating)
    if cr:
        c.rating_sum -= cr.rating
    else:
        cr = db.CourseRate()
        db.add(cr)
        cr.course_id = id
        cr.user_id = uid
        c.rater_sum += 1
    c.rating_sum += rating
    cr.rating = rating
    cr.comment = comment
    cr.anonymous = int(anonymous)
    db.commit()
    return ""


# 课程评价列表
def rate_list(id, page):
    q = db.CourseRate.query.filter(db.CourseRate.course_id == id).order_by(db.CourseRate.time.desc()).offset(
        page*config.page_size).limit(config.page_size).all()
    out = []
    uid = user.now_uid
    for i in q:
        dic = {'id': i.id, 'course_id': i.course_id,
               'rating': i.rating, 'comment': i.comment, 'time': i.time.timestamp(),
               'anonymous': i.anonymous, 'like_sum': i.like_sum}
        like = db.CourseRateLike.query.filter(
            db.CourseRateLike.rate_id == i.id, db.CourseRateLike.user_id == uid).first()
        dic['like'] = (like and like.like)
        if not i.anonymous:
            dic['user'] = {'id': i.user.id,
                           'nickname': i.user.nickname, 'avatar': i.user.avatar}
        out.append(dic)
    return out


# 评教点赞
def rate_like(id, like):
    uid = user.now_uid
    q = db.CourseRateLike.query.filter(
        db.CourseRateLike.rate_id == id, db.CourseRateLike.user_id == uid).first()
    cr=db.CourseRate.query.filter_by(id=id).first()
    if not cr: 0/0
    cr.like_sum+=like
    if q:
        cr.like_sum-=q.like
        q.like=like
    elif like:
        q=db.CourseRateLike(rate_id=id,user_id=uid)
        db.add(q)
    db.commit()
    return ""


# 课程列表
def search(course_search, teacher_search, page):
    if (not course_search) and (not teacher_search):
        return []
    q = db.Course.query.filter(
        or_(db.Course.name.like("%{}%".format(course_search)),
            db.Course.number.like("%{}%".format(course_search))),
        db.Course.teachers_name.like("%{}%".format(teacher_search))).offset(
        page*config.page_size).limit(config.page_size).all()
    return [db.to_dict(i) for i in q]
