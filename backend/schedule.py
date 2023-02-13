'''
Author: flwfdd
Date: 2023-02-13 20:04:10
LastEditTime: 2023-02-14 00:06:17
Description: 课程表
_(:з」∠)_
'''
import webvpn
import icalendar
import datetime
import uuid
import saver

time_table=[
    [[8,0],[8,45]],
    [[8,50],[9,35]],
    [[9,55],[10,40]],
    [[10,45],[11,30]],
    [[11,35],[12,20]],
    [[13,20],[14,5]],
    [[14,10],[14,55]],
    [[15,15],[16,0]],
    [[16,5],[16,50]],
    [[16,55],[17,40]],
    [[18,30],[19,15]],
    [[19,20],[20,5]],
    [[20,10],[20,55]],
]


def get_time(first_day,week,day,class_number,type): #end_type=0为上课时间 1为下课时间
    return first_day+datetime.timedelta(days=(week-1)*7+day-1,hours=time_table[class_number-1][type][0],minutes=time_table[class_number-1][type][1])


def get_ics_url(cookie,term=''):
    dic=webvpn.get_schedule(cookie,term)

    cal=icalendar.Calendar()
    cal['VERSION']='2.0'
    cal['X-WR-CALNAME']='BIT101课程表'
    cal['PRODID']='BIT101 '+str(datetime.datetime.now())
    cal['TZID']='Asia/Shanghai'
    first_day=datetime.datetime.strptime(dic['first_day'],r'%Y-%m-%d')
    class_ct=0
    time_ct=0
    for i in dic['data']:
        for j in range(len(i['SKZC'])):
            if int(i['SKZC'][j]):
                event=icalendar.Event()
                event['UID']=uuid.uuid4()
                event['SUMMARY']=i['KCM'] #课程名
                event['LOCATION']=i['JASMC'] #地址
                event['DESCRIPTION']=str(i['JASMC'])+' | '+str(i['SKJS']) + ' | '+str(i['YPSJDD']) #描述
                event.add('DTSTART',get_time(first_day,j+1,i['SKXQ'],i['KSJC'],0))
                event.add('DTEND',get_time(first_day,j+1,i['SKXQ'],i['JSJC'],1))
                cal.add_component(event)

                class_ct+=1
                time_ct+=45*(i['JSJC']-i['KSJC']+1)

    return {'url':saver.upload_tmp(cal.to_ical(),str(uuid.uuid4())+'.ics'),'msg':'一共添加了{}学期的{}节课，合计坐牢时间{}小时（雾'.format(dic['term'],class_ct,round(time_ct/60))}

