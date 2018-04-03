# -*- coding: utf-8 -*-
# @Date    : 2018-03-31 12:17:57
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts,to_dict
from common.sitemail import sitemail
from common.security import encrypt_string,decrypt_string
from models.users import users
from models.course import course, course_temp, temp_to_course
from models.user_to_course import user_to_course,collect
from models.change_email import change_email
from models.jitang import jitang
from models.__init__ import db_session
from sqlalchemy import asc,desc
from _decorator import login_required,self_login_required
from urllib import unquote
import logging
import random
import re

page = Blueprint('resouce_manage',__name__)


@page.route('/course/manage')
def course_manage():
    user = users.query.filter(users.email == session['email']).first()
    courses = course_temp.query.filter(course.user_id == user.id).all()
    if courses:
        for c in courses:
            c.str_create_date = c.create_date.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('manage/course_manage.html',courses=courses)

@page.route('/course/new',methods=['POST','GET'])
def course_new():
    ''' 新建课程，先存入course_temp '''
    if request.method != 'POST':
        return 'fail'

    try:
        user = users.query.filter(users.email==escape(session['email'])).first()
        course_title = unquote(request.form.get('course_title'))
        pic = request.form.get('pic')
        desc = unquote(request.form.get('desc'))
    except Exception,e:
        return 'fail'

    confirm = course_temp.query.filter(course_temp.title == course_title).first()
    confirm2 = course.query.filter(course.title == course_title).first()
    if confirm or confirm2:
        return u'此课程名字已存在，请重新输入！'

    new_course = course_temp(title=course_title, item_image=pic, description = desc, user_id = user.id)
    db_session.add(new_course)
    db_session.commit()

    return 'success'

@page.route('/course/manage/<int:courseid>')
#需要验证是否为当前用户
def video_manage(courseid):

    return render_template('manage/lesson_manage.html')


