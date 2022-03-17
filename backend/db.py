'''
Author: flwfdd
Date: 2022-03-09 13:37:03
LastEditTime: 2022-03-09 22:16:44
Description: 数据库
_(:з」∠)_
'''
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
import datetime

db = SQLAlchemy()


def add(x):
    db.session.add(x)


def commit():
    db.session.commit()


def to_json(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(24), unique=True, nullable=False)
    name = db.Column(db.String(24))
    birthday = db.Column(db.String(24))
    account_type = db.Column(db.String(24))
    class_name = db.Column(db.String(24))
    college = db.Column(db.String(24))
    major = db.Column(db.String(24))
    sex = db.Column(db.String(4))
    nickname = db.Column(db.String(24), default="BITself")
    avatar=db.Column(db.String(42),default="3c3b31a4dc49c0224ebcf93a3f70790c.PNG")
    motto = db.Column(
        db.Text, default="I offer you the BITterness of a man who has looked long and long at the lonely moon.")
    register_time=db.Column(db.DateTime, default=datetime.datetime.now)

class Image(db.Model):
    id=db.Column(db.String(42), primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(424), nullable=False)
    time=db.Column(db.DateTime, default=datetime.datetime.now)
    user=db.Column(db.Integer,db.ForeignKey('user.id'))