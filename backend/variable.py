'''
Author: flwfdd
Date: 2022-07-28 13:08:11
LastEditTime: 2022-07-28 14:43:47
Description: 储存变量的模块
_(:з」∠)_
'''
import db


def get(obj):
    q = db.Variable.query.filter_by(obj=obj).first()
    return q.data


def post(obj, data):
    q = db.Variable.query.filter_by(obj=obj).first()
    if not q:
        q = db.Variable(obj=obj)
        db.add(q)
    q.data = data
    db.commit()
    return q.data


def init():
    l = [
        ('carousel', '[]')
    ]
    for i in l:
        q = db.Variable.query.filter_by(obj=i[0]).first()
        if not q:
            db.add(db.Variable(obj=i[0], data=i[1]))
    db.commit()
