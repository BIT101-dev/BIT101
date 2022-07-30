'''
Author: flwfdd
Date: 2022-05-29 14:53:56
LastEditTime: 2022-07-30 23:58:53
Description: 
_(:з」∠)_
'''
import numbers
import db
import config
from sqlalchemy import and_, or_
import reaction
import saver
import user
import datetime


# 单个课程详情
def detail(id):
    course = db.Course.query.filter_by(id=id).first()
    dic = db.to_dict(course)
    dic['like'] = reaction.get_like_status('course'+str(dic['id']))
    return dic


# 课程列表
def list(search, order, page):
    page = int(page)
    q = db.Course.query
    if search:
        q = q.filter(
            or_(db.Course.name.like("%{}%".format(search)),
                db.Course.number.like("%{}%".format(search)),
                db.Course.teachers_name.like("%{}%".format(search)),
                db.Course.teachers_number.like("%{}%".format(search)),))

    if order == 'like':
        q = q.order_by(db.Course.like_num.desc())
    elif order == 'comment':
        q = q.order_by(db.Course.comment_num.desc())
    elif order == 'rate':
        q = q.order_by(db.Course.rate.desc())
    else:
        q = q.order_by(db.Course.update_time.desc())

    q = q.offset(page*config.page_size).limit(config.page_size).all()
    return db.to_dict(q)


# 获取上传链接
def upload_url(number, tp, name):
    c = db.Course.query.filter_by(number=number).first()
    if not c:
        return False
    if tp not in ['book', 'ppt', 'exam']:
        tp = 'other'
    path = 'course/{}/{}/{}'.format(c.name+'-'+number, tp, name)
    url = saver.onedrive_upload_url(path)
    if not url:
        return False
    q = db.CourseUploadLog.query.filter(and_(
        db.CourseUploadLog.user == user.now_uid,
        db.CourseUploadLog.number == number,
        db.CourseUploadLog.type==tp,
        db.CourseUploadLog.name==name)).first()
    if not q:
        q=db.CourseUploadLog(user=user.now_uid,number=number,type=tp,name=name,course_name=c.name)
        db.add(q)
        db.commit()
    return {'url': url, 'id':q.id}


readme_template='''
# BIT101 {course_name} 课程共享资料
> 课程编号：{number}

本页面由[BIT101]({main_url})维护，[点击查找 {course_name} 课程及评价]({main_url}/course/?search={number})

## 类别说明
* 书籍(book)：教科书、课程相关电子书等
* 课件(ppt)：PPT什么的
* 考试(exam)：考试相关的往年题、复习资料等
* 其他(other)：兜底条款，比如作业资料....？

## 文件上传记录和说明

'''

log_template='''
* `/{type}/{name}`@`{time}`
{msg}
'''

def upload_log(id,msg):
    q=db.CourseUploadLog.query.filter_by(id=id).first()
    if not (q and str(q.user)==str(user.now_uid)): return False
    q.msg=msg
    q.finish=True

    map_dict={
        'name':q.name,
        'main_url':config.main_url,
        'number':q.number,
        'msg':msg,
        'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type':q.type,
        'course_name':q.course_name
    }
    r=db.CourseUploadReadme.query.filter_by(number=q.number).first()
    if not r:
        r=db.CourseUploadReadme(text=readme_template.format_map(map_dict),number=q.number)
        db.add(r)
    r.text+=log_template.format_map(map_dict)
    
    saver.onedrive_upload_file('course/{}/README.md'.format(q.course_name+'-'+q.number),str(r.text).encode('utf-8'))
    db.commit()
    return True
