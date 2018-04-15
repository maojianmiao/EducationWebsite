# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 22:07:07
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts,to_dict
from models.users import users
from models.course import course
from models.change_email import change_email
from models.__init__ import db_session
from sqlalchemy import asc,desc
from urllib import unquote
import logging
import re

page = Blueprint('search',__name__)

@page.route('/search',methods=['GET','POST'])
def search():
    c_type = request.args.get('type')
    text = unquote(request.args.get('text'))
    logging.info(text)
    if c_type == 'course':
        courses = course.query.filter(course.status==1,course.title.like(u'%{}%'.format(text))).all()
    else:
        courses = course.query.join(users, course.user_id == users.id).filter(course.status==1,users.name.like(u'%{}%'.format(text))).all()

    logging.info(courses)
    course_count = len(courses)

    return render_template('search/search.html',courses=courses, course_count=course_count,text=text)

@page.route('/input/refer')
def input_refer():
    text = unquote(request.args.get('text'))
    items = 6 #一次最多返回多少个提示
    if not text:
        return ''
    courses = course.query.filter(course.status==1,course.title.like(u'%{}%'.format(text))).order_by(desc(course.view)).slice(0,items).all()
    if not courses:
        return ''
    return render_template('search/refer.html',courses=courses)

