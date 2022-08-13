'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-08-13 21:57:54
Description: 
_(:з」∠)_
'''
from flask import Flask
import csv
import sys 
sys.path.append("..") 
import db
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.db.app = app
db.db.init_app(app)
db.db.create_all()

f=open("2021-2022-2.csv","r")
dic=csv.DictReader(f)

def get_teachers(name_l,number_l):
    out=[]
    for i in range(len(number_l)):
        q = db.Teacher.query.filter_by(number=number_l[i]).first()
        if q:
            out.append(q)
        else:
            out.append(db.Teacher(number=number_l[i],name=name_l[i].replace("[辅讲]","")))
    return out

for i in dic:
    name_l=i['上课教师'].split(',')
    number_l=i['教师号'].split(',')
    courses = db.Course.query.filter_by(number=i['课程号']).all()
    i['课程名']=i['课程名'].replace('/','_')
    for j in courses:
        if not j.name==i['课程名']:
            print(j.name,i['课程名'])
        number_ll=[x.number for x in j.teachers]
        if sorted(number_ll)==sorted(number_l):
            break
    else:
        course=db.Course()
        course.number=i['课程号']
        course.name=i['课程名']
        course.teachers_name=i['上课教师']
        course.teachers=get_teachers(name_l,number_l)
        course.teachers_number=','.join([i.number for i in course.teachers])
        db.add(course)
        q=db.CourseUploadReadme.query.filter_by(number=course.number).first()
        if not q: db.add(db.CourseUploadReadme(number=course.number))
        db.commit()