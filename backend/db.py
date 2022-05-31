'''
Author: flwfdd
Date: 2022-03-09 13:37:03
LastEditTime: 2022-05-31 00:40:46
Description: 数据库
_(:з」∠)_
'''
from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
import datetime

db = SQLAlchemy()


def add(x):
    db.session.add(x)


def add_all(x):
    db.session.add_all(x)


def commit():
    db.session.commit()


def to_json(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(24), unique=True, nullable=False)  # 学号
    password = db.Column(db.String(42), nullable=False)
    nickname = db.Column(db.String(24), unique=True,)
    avatar = db.Column(
        db.String(42), default="")
    motto = db.Column(
        db.Text, default="I offer you the BITterness of a man who has looked long and long at the lonely moon.")
    register_time = db.Column(db.DateTime, default=datetime.datetime.now)


# 图床
class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.String(42), primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(424), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    user = db.Column(db.Integer, db.ForeignKey('user.id')) #上传者


# 课程老师多对多关系表
course_teacher_table = db.Table('course_teacher_table',
                                db.Column('course_id', db.Integer, db.ForeignKey(
                                    'course.id'), primary_key=True),
                                db.Column('teacher_id', db.Integer, db.ForeignKey(
                                    'teacher.id'), primary_key=True)
                                )


# 课程
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(24))
    name = db.Column(db.String(224), nullable=False)
    rating_sum = db.Column(db.Integer, default=0)
    rater_sum = db.Column(db.Integer, default=0)
    teachers_name = db.Column(db.String(224), nullable=False)
    teachers = db.relationship(
        'Teacher', secondary=course_teacher_table, backref=db.backref('courses'))
    rates = db.relationship("CourseRate", backref='course')


# 老师
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(24), unique=True)
    name = db.Column(db.String(42), nullable=False)


# 课程评分
class CourseRate(db.Model):
    __tablename__ = 'course_rate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey(
        "course.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    like_sum = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, default=datetime.datetime.now,
                     onupdate=datetime.datetime.now)
    user = db.relationship("User", backref='course_comments')


# 课程评分点赞
class CourseRateLike(db.Model):
    __tablename__ = 'course_rate_like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    rate_id = db.Column(db.Integer, nullable=False)
    like = db.Column(db.Boolean, default=True)
    time = db.Column(db.DateTime, default=datetime.datetime.now,
                     onupdate=datetime.datetime.now)
