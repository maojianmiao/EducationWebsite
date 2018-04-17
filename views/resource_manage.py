# -*- coding: utf-8 -*-
# @Date    : 2018-03-31 12:17:57
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts,to_dict,get_page_seq
from models.users import users
from models.video import video
from models.course import course
from models.category import category,category_to_course
from models.__init__ import db_session
from sqlalchemy import asc,desc,func
from _decorator import login_required,admin_required,self_required
from datetime import datetime
from urllib import unquote
from werkzeug import secure_filename
import types
import time
import logging
import re
import traceback

page = Blueprint('resouce_manage',__name__)


@page.route('/course/manage')
@login_required
def course_manage():
    try:
        page_id = int(request.args.get('pid'))
    except Exception,e:
        logging.warning(e)
        page_id = 1

    user = users.query.filter(users.email == session['email']).first()
    items = 24 #控制每页显示课程的数量
    count = db_session.query(func.count(course.id)).filter(course.user_id == user.id).first()[0]
    pageseq = get_page_seq(count, items)
    courses = course.query.filter(course.user_id == user.id).order_by(desc(course.create_date)).slice(page_id*items - items, page_id *items).all()
    
    if courses:
        for c in courses:
            c.str_create_date = c.create_date.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('manage/course_manage.html',courses=courses,pageseq=pageseq)

@page.route('/course/new',methods=['POST','GET'])
@login_required
def course_new():
    ''' 新建课程 '''
    if request.method != 'POST':
        return render_template('manage/course_create.html')

    try:
        user = users.query.filter(users.email==escape(session['email'])).first()
        course_title = unquote(request.form.get('course_title'))
        pic = request.form.get('pic')
        desc = unquote(request.form.get('desc'))
        category_id = int(request.form.get('category_id'))
        sub_id = request.form.get('sub_id')
    except Exception,e:
        return 'fail'

    if sub_id == 'null':
        sub_id = None
    else:
        sub_id = int(sub_id)
    #confirm2 = course_temp.query.filter(course_temp.title == course_title).first()
    confirm = course.query.filter(course.status==1,course.title == course_title).first()
    if confirm:
        return u'此课程名字已存在，请重新输入！'

    new_course = course(title=course_title, item_image=pic, description = desc, user_id = user.id)
    nc_relation = category_to_course(course=new_course,category_id_first=category_id,category_id_second=sub_id)
    db_session.add(new_course)
    db_session.add(nc_relation)
    db_session.commit()

    return 'success'

@page.route('/course/manage/<int:courseid>')
@self_required #需要验证是否为当前用户
def video_manage(courseid):
    session['ccid'] = courseid
    user = users.query.filter(users.email == session['email']).first()
    lessons = video.query.filter(video.course_id == int(courseid)).all()
    for l in lessons:
        l.str_create_date = l.create_date.strftime('%Y-%m-%d %H:%M:%S')
    c_course = course.query.filter(course.id == courseid).first()

    index = category_to_course.query.filter(category_to_course.course_id == courseid).order_by(desc(category_to_course.id)).first()
    if not index:
        level1 = u'未定义'
        level2 = ''

    if index:
        level1 = category.query.filter(category.id == index.category_id_first).first().category_name
        if index.category_id_second:
            level2 = '/' + category.query.filter(category.id == index.category_id_second).first().category_name
        else:
            level2 = ''
    else:
        level2 = ''
    return render_template('manage/lesson_manage.html',course=c_course,lessons=lessons,user=user,level1=level1,level2=level2)

@page.route('/subselect/<int:pre_id>')
def sub_select(pre_id):
    subs = category.query.filter(category.pre_category_id == pre_id).all()

    return render_template('manage/subselect.html',subs=subs)

@page.route('/course/del',methods=['POST'])
@login_required
def del_course():
    try:
        items = request.form.get('items')
    except Exception,e:
        logging.info(e)
        return 'fail'

    l_items = items.split(',')
    for i in l_items:
        if i:
            current = course.query.filter(course.id == int(i)).first()
            relation = category_to_course.query.filter(category_to_course.course_id == int(i)).first()
            if current:
                db_session.delete(current)
            if relation:
                db_session.delete(relation)
    db_session.commit()
    return 'success'

@page.route('/new/upload',methods=['POST'])
@login_required
def upload_file():
    file_path = 'D:/resource/videos/{}'
    if request.method == 'POST':
        #request。files中的存储上传文件类的key对应表单中input的name属性
        f = request.files['fileUpload']
        logging.info(type(f))
        try:
            sf = secure_filename(f.filename)
            hashString = hash_string(f.read())

            #存储名字重新生成
            #=文件的sha1值+原有后缀
            newName = hashString + '.' + sf.split('.')[-1]

            f.seek(0)
            f.save(file_path.format(newName))
            print file_path.format(newName)
            return '//video.lyl.com/{}'.format(newName)
        except Exception,e:
            logging.error(e)
            return ''

@page.route('/course/edit',methods=['POST','GET'])
def course_edit():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        if request.form.get('sub_id') == 'null':
            sub_id = None
        else:
            sub_id = int(request.form.get('sub_id'))

        c = course.query.filter(course.id == int(course_id)).first()
        c.title = request.form.get('course_title')
        c.item_image = request.form.get('pic')
        c.description = request.form.get('desc')
        c.status = 3 ###课程状态0: 未审核；1：已审核；2：审核中 3：已修改
        relation = category_to_course.query.filter(category_to_course.course_id==course_id).order_by(desc(category_to_course.id)).first()
        
        if not relation:
            relation = category_to_course(course_id,int(request.form.get('category_id')),sub_id)
            db_session.add(relation)
        else:
            relation.category_id_first = int(request.form.get('category_id'))
            relation.category_id_second = sub_id
        
        db_session.commit()
        return 'success'
    
    try:
        course_id = int(request.args.get('course_id'))
    except Exception,e:
        return 'fail'

    c = course.query.filter(course.id==course_id).first()
    cc_relation = category_to_course.query.filter(category_to_course.course_id == course_id).order_by(desc(category_to_course.id)).first()
    return render_template('manage/course_edit.html',course=c, category=cc_relation)

@page.route('/course/audit',methods=['POST','GET'])
def course_audit():
    try:
        items = request.form.get('items')
    except Exception,e:
        logging.info(e)
        return 'fail'

    items = items.split(',')

    for item in items:
        if item:
            current = course.query.filter(course.id == int(item)).first()
            current.status = 2 #提交审核，状态改为2。课程状态0: 未审核；1：已审核；2：审核中 3：已修改

    db_session.commit()
    return 'success'


@page.route('/lesson/new',methods=['POST','GET'])
def lesson_new():
    ''' 新建课时视频 '''
    if request.method != 'POST':
        c = course.query.filter(course.id == session['ccid']).first()
        return render_template('manage/lesson_create.html', course=c)

    try:
        user = users.query.filter(users.email==escape(session['email'])).first()
        video_title = unquote(request.form.get('video_title'))
        video_url = request.form.get('video_url')
        v_desc = unquote(request.form.get('desc'))
        course_id = int(request.form.get('course_id'))
        duration = request.form.get('duration')
        duration = round(float(duration), 2)
    except Exception,e:
        print traceback.print_exc()
        logging.info(e)
        return 'fail'

    sql_order = video.query.filter(video.course_id == int(course_id)).order_by(desc(video.order)).first()
    current_course = course.query.filter(course.id == course_id).first()
    current_course.status = 3 #课程的任何信息有改动都把课程状态设置为3：已修改，防止未审核的内容发布给用户


    if sql_order:
        order = sql_order.order + 1
    else:
        order = 1
    new_video = video(title=video_title,video_url=video_url,description=v_desc,course_id=course_id,duration=duration,order=order)
    session['order_{}'.format(course_id)] = order
    db_session.add(new_video)
    db_session.commit()
    return 'success'

@page.route('/lesson/edit', methods=['POST','GET'])
def edit_lesson():
    if request.method != 'POST':
        vid = int(request.args.get('vid'))
        current_video = video.query.filter(video.id == vid).first()
        return render_template('manage/lesson_edit.html', lesson=current_video,course=current_video.course)

    try:
        user = users.query.filter(users.email==escape(session['email'])).first()
        video_title = unquote(request.form.get('video_title'))
        video_url = request.form.get('video_url')
        v_desc = unquote(request.form.get('desc'))
        course_id = int(request.form.get('course_id'))
        duration = request.form.get('duration')
        vid = int(request.form.get('vid'))
    except Exception,e:
        print traceback.print_exc()
        logging.info(e)
        return 'fail'

    v = video.query.filter(video.id == vid).first()
    c = course.query.filter(course.id == course_id).first()
    ##课程的任何信息有改动都把课程状态设置为3：已修改，防止未审核的内容发布给用户
    c.status = 3
    v.status = 3

    v.title = video_title
    v.video_url = video_url
    v.description = v_desc
    v.duration = round(float(duration),2)

    db_session.commit()
    return 'success'

@page.route('/lesson/del',methods=['POST'])
def del_lesson():
    if request.method != 'POST':
        return 'fail'

    cid = request.form.get('cid')
    items = request.form.get('items')
    for item in items.split(','):
        if not item:
            continue
        v =  video.query.filter(video.id == int(item)).first()
        v.status = 5

    c = course.query.filter(course.id == int(cid)).first()
    c.status = 3

    db_session.commit()
    return 'success'

@page.route('/course/admin/audit',methods=['GET','POST'])
@admin_required
def audit_course():
    if request.method == 'POST':
        try:
            items = request.form.get('items').split(',')
        except Exception,e:
            logging.info(e)
            return 'fail'

        for cid in items:
            if not cid:
                continue
            current_course = course.query.filter(course.id == int(cid)).first()
            current_course.status = 1 #审核通过

            videos = video.query.filter(video.course_id == int(cid)).all()
            for v in videos:
                print v.status, type(v.status),v.id
                if int(v.status) == 5:
                    print 'delete %s' % v.id
                    db_session.delete(v)
                    continue
                v.status = 1 #审核通过，把视频状态都改一下

        db_session.commit()
        
        return 'success'

    try:
        page_id = int(request.args.get('pid'))
    except Exception,e:
        logging.warning('no item: %s',e)
        page_id = 1

    items = 22 #控制每页显示课程的数量
    count = db_session.query(func.count(course.id)).filter(course.status == 2).first()[0]
    logging.info('count: %s',count)
    courses = course.query.filter(course.status == 2).slice(page_id*items - items, page_id *items).all()
    if courses:
        for c in courses:
            c.str_create_date = c.create_date.strftime('%Y-%m-%d %H:%M:%S')

    pageseq = get_page_seq(count, items)
    logging.info('pageseq: %s' ,pageseq)

    return render_template('manage/course_audit.html', courses = courses, pageseq = pageseq)


@page.route('/course/admin/audit/<int:courseid>')
@admin_required
def lesson_audit(courseid):
    session['ccid'] = courseid
    user = users.query.filter(users.email == session['email']).first()
    lessons = video.query.filter(video.course_id == int(courseid)).all()
    for l in lessons:
        l.str_create_date = l.create_date.strftime('%Y-%m-%d %H:%M:%S')
    c_course = course.query.filter(course.id == courseid).first()
    
    index = category_to_course.query.filter(category_to_course.course_id == courseid).order_by(desc(category_to_course.id)).first()
    if not index:
        level1 = u'未定义'
        level2 = ''

    if index:
        level1 = category.query.filter(category.id == index.category_id_first).first().category_name
        if index.category_id_second:
            level2 = '/' + category.query.filter(category.id == index.category_id_second).first().category_name
        else:
            level2 = ''
    else:
        level2 = ''

    return render_template('manage/lesson_audit.html',course=c_course,lessons=lessons,user=user, level1=level1, level2=level2)

@page.route('/course/admin/refuse',methods=['POST'])
@admin_required
def refuse_course():
    if request.method == 'POST':
        try:
            items = request.form.get('items').split(',')
        except Exception,e:
            logging.info(e)
            return 'fail'
        for cid in items:
            if not cid:
                continue
            current_course = course.query.filter(course.id == int(cid)).first()
            current_course.status = 4 #审核驳回
        db_session.commit()
        return 'success'