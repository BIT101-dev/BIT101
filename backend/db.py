'''
Author: flwfdd
Date: 2022-03-09 13:37:03
LastEditTime: 2022-03-09 22:16:44
Description: 数据库
_(:з」∠)_
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def add(x):
    db.session.add(x)
    db.session.commit()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(24), unique=True, nullable=False)
    name = db.Column(db.String(24))
    birthday = db.Column(db.String(24))
    account_type = db.Column(db.String(24))
    class_name = db.Column(db.String(24))
    college = db.Column(db.String(24))
    sex = db.Column(db.String(4))