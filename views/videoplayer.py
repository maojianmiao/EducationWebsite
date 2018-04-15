# -*- coding: utf-8 -*-
# @Date    : 2018-02-24 15:31:12
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts,to_dict
from models.users import users
from models.change_email import change_email
from models.video import video
from models.course import course
from models.comment import comment
from models.note import note
from models.video_record import video_record
from models.user_to_course import user_to_course, collect
from models.course_rate import course_rate
from models.__init__ import db_session
from sqlalchemy import asc,desc,func
from _decorator import login_required
from datetime import datetime
from urllib import unquote
import types
import time
import logging
import re

page = Blueprint('videoplayer',__name__)


@page.route('/play/lesson')
@login_required
def play_lesson():
    """ url 必须包含courseid和videoid """
    return_dict = {}
    try:
        courseid = int(request.args.get('courseid'))
        videoid = int(request.args.get('videoid'))
    except:
        return redirect(url_for('index.error'))
    #当前登录的用户
    user = users.query.filter(users.email == escape(session['email'])).first()

    if not courseid or not videoid:
        return redirect(url_for('index.error'))

    video_info = video.query.filter(video.id == videoid,video.course_id == courseid).first()
    if not video_info:
        return redirect(url_for('index.error'))
        
    course_info = course.query.filter(course.id == courseid).first()
    #查出上一课时和下一课时
    pre_order,next_order = int(video_info.order) - 1,int(video_info.order) + 1
    pre_video = video.query.filter(video.course_id == courseid,video.order == pre_order).first()
    next_video = video.query.filter(video.course_id == courseid,video.order == next_order).first()

    if pre_video:
        pre_title = pre_video.title
        pre_video_url = '/play/lesson?courseid={}&videoid={}'.format(courseid,pre_video.id)
    else:
        pre_title = "无"
        pre_video_url = "#"

    if next_video:
        next_title = next_video.title
        next_video_url = '/play/lesson?courseid={}&videoid={}'.format(courseid,next_video.id)
    else:
        next_title = "无"
        next_video_url = '#'

    comments = comment.query.filter(comment.course_id == courseid).all()
    count = len(comments)
    pages = (count -1) / 30 + 1
    if pages > 1 and pages <= 11:
        pageseq = list(range(1,pages + 1))
    elif pages > 11:
        pageseq = list(range(1,10))
        pageseq += ['...',pages]
    else:
        pageseq = None
    
    
    commentItems = getComment(courseid,1)
    logging.info(repr(commentItems))

    #查询用户笔记
    note_items = note.query.filter(note.user_id==user.id,note.video_id==videoid).order_by(desc(note.id)).all()
    for i in note_items:
        i.str_create_date = i.create_date.strftime('%Y-%m-%d %H:%M:%S')

    #配置要返回给html模板的变量
    return_dict['video_url'] = video_info.video_url
    return_dict['title'] = video_info.title
    return_dict['course_title'] = course_info.title
    return_dict['order'] = video_info.order
    return_dict['author'] = users.query.filter(users.id==course.user_id).first().name
    return_dict.update(pre_title=pre_title)
    return_dict.update(pre_video_url=pre_video_url)
    return_dict.update(next_title=next_title)
    return_dict.update(next_video_url=next_video_url)
    return_dict.update(notes=note_items) #笔记字典
    return_dict.update(course=course_info) #课程字典
    return_dict.update(video=video_info) #视频字典
    return_dict.update(commentItems=commentItems) #评论列表
    return_dict.update(user=user) #用户字典
    return_dict.update(pageseq=pageseq) #评论分页控制
    return render_template('videoplayer/video.html',**return_dict)

#添加评论
@page.route('/add/comment',methods=['POST'])
@login_required
def addComment():
    if request.method == 'POST':
        courseid = request.form.get('courseid')
        videoid = request.form.get('videoid')
        comment_text = request.form.get('comment')
        
        user = users.query.filter(users.email == session['email']).first()
        
        #创建一个评论实例
        com = comment(comment=comment_text,video_id=videoid,course_id=courseid,users=user)
        com.str_create_date = com.create_date.strftime('%Y-%m-%d %H:%M:%S')
        #添加数据到orm中间层
        db_session.add(com)
        #提交数据
        db_session.commit()

    return render_template('videoplayer/comment.html',comment=com,user=user)


#添加笔记
@page.route('/add/note',methods=['POST'])
@login_required
def addNote():
    if request.method == 'POST':
        courseid = request.form.get('courseid')
        videoid = request.form.get('videoid')
        note_text = request.form.get('note')

        user = users.query.filter(users.email == session['email']).first()

        current_note = note(note_text, users=user, course_id=courseid, video_id=videoid)
        current_note.str_create_date = current_note.create_date.strftime('%Y-%m-%d %H:%M:%S')
        db_session.add(current_note)
        db_session.commit()


    return render_template('videoplayer/note.html',user=user,note=current_note)

@page.route('/pages/<page>')
def paging(page):
    courseid = request.args.get("courseid")

    commentItems = getComment(courseid,int(page))
    logging.info(repr(commentItems))

    return render_template('videoplayer/comments.html',commentItems=commentItems)


#@page.route('/comment/list')
def getComment(courseid,page,items=30):
    """ items：一页显示多少个评论

        page:第几页 """
    #courseid = int(request.args.get('courseid'))
    #page = int(request.args.get('page'))
    #email = escape(session['email'])
    comments = comment.query.filter(comment.course_id == courseid).order_by(desc(comment.create_date)).slice(page*items - items, page *items).all()

    for i in comments:
        if type(i) is not types.StringType:
            i.str_create_date = i.create_date.strftime('%Y-%m-%d %H:%M:%S')
        i.user = users.query.filter(users.id == i.user_id).first()

    return comments


@page.route("/video/record",methods=['POST'])
@login_required
def video_recodrd():
    """  请求链接需要提交的数据
        {
            courseid:xx,
            videoid:xx,
            current_time:xxxx
        }"""
    
    user = users.query.filter(users.email == session['email']).first()
    videoid = int(request.form.get('videoid'))

    if request.method == 'POST':
        try:
            courseid = int(request.form.get('courseid'))
            current_time = request.form.get('current_time')
            
            record = video_record.query.filter(video_record.user_id == user.id, video_record.video_id == videoid).first()
            if record:
                record.play_time = current_time
            else:
                record = video_record(users=user, course_id=courseid, video_id=videoid,play_time=current_time)
                db_session.add(record)
            
            db_session.commit()
            return 'success'
        except Exception,e:
            logging.error(e)
            return 'fail'

@page.route('/video/record/get',methods=['GET'])
@login_required
def get_record():
    user = users.query.filter(users.email == session['email']).first()
    videoid = int(request.args.get('videoid'))
    if request.method == 'GET':
        try:
            logging.info('here here')
            record = video_record.query.filter(video_record.user_id==user.id,video_record.video_id == videoid).\
            order_by(desc(video_record.id)).first()
            if record:
                return str(record.play_time)
            else:
                return '0'
        except Exception,e:
            logging.error(e)
            return '0'

@page.route('/course/<int:courseid>')
@login_required
def get_course(courseid):
    user = users.query.filter(users.email == session['email']).first() 
    
    #每次进入课程详情页的时候，写下用户观看课程的记录
    course_record = user_to_course.query.filter(user_to_course.course_id == courseid, user_to_course.user_id == user.id).first()
    if not course_record:
        add_record = user_to_course(user.id, courseid)
        db_session.add(add_record)
        logging.info('add record: %s ', add_record)

    #当前登录用户对这个课程的评分
    current_user_rate = course_rate.query.filter(course_rate.user_id == user.id, course_rate.course_id == courseid).first()

    #当前课程信息
    current_course = course.query.filter(course.id == int(courseid)).first()
    #课程所有视频信息
    lessons = video.query.filter(video.course_id == int(courseid)).order_by(asc(video.order)).all()

    learners = db_session.query(func.count(user_to_course.id)).filter(user_to_course.course_id == courseid).first()
    rate_count = db_session.query(func.count(course_rate.id),func.sum(course_rate.score))\
    .filter(course_rate.course_id == courseid).first()
    logging.info('rate people: %s, rates: %s, learners: %s',rate_count[0],rate_count[1], learners[0])
    
    if learners:
        current_course.view = learners[0]
    if rate_count[0] > 0:
        current_course.score_count = rate_count[0]
    if rate_count[1]:
        current_course.score = rate_count[1] / float(rate_count[0])

    for v in lessons:
        v.format_duration = '%02d:%02d' % (int(v.duration /60), int(v.duration % 60))
        current_record = video_record.query.filter(video_record.user_id == user.id, video_record.video_id==v.id).first()
        if current_record and current_record.is_finished == '1':
            v.progress = u'{:>6}'.format('已完成')
        elif current_record and current_record.is_finished == '0':
            v.progress = '{:>6}%'.format(round(current_record.play_time / float(v.duration) * 100, 2))
        else:
            v.progress = u'{:>6}'.format(' 未开始')

    rates = course_rate.query.filter(course_rate.course_id == courseid)\
    .order_by(desc(course_rate.create_date)).slice(0, 5).all()
    
    for i in rates:
        i.str_create_date = i.create_date.strftime('%Y-%m-%d %H:%M:%S')
    db_session.commit()

    is_collect = collect.query.filter(collect.user_id == user.id, collect.course_id == courseid).first()
    return render_template('videoplayer/course.html',course=current_course,lessons=lessons, rates=rates, current_user_rate = current_user_rate, is_collect = is_collect)

@page.route('/course/score',methods=['GET'])
@login_required
def add_score():
    user = users.query.filter(users.email == session['email']).first() 

    try:
        course_id = int(request.args.get('course_id'))
        comment = unicode(unquote(request.args.get('comment')))
        score = int(float(request.args.get('score')) * 2)
    except Exception,e:
        logging.error(e)
        return ''

    rate = course_rate(score, comment, course_id=course_id, user=user)
    
    db_session.add(rate)
    db_session.commit()

    return render_template('videoplayer/rate_comment.html', rate=rate)