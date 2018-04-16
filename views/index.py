# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 00:04:25
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,send_from_directory,send_file
from sqlalchemy import asc,desc,func
from common.api import hash_string, get_page_seq
from werkzeug import secure_filename
from models.__init__ import db_session
from models.course import course
from models.users import users
from models.jitang import jitang
from models.category import category, category_to_course
import os
import logging
page = Blueprint('index',__name__)

#两个路径连接到一个页面
@page.route('/')
@page.route('/index')
def index():
    try:
        username = escape(session['username'])
    except:
        username = None

    categorys = category.query.filter(category.level==1).all()
    #logging.info(categorys)
    for item in categorys:
        
        item.courses = course.query.join(category_to_course, category_to_course.course_id == course.id).\
        filter(category_to_course.category_id_first == item.id,course.status==1).slice(0,8).all()
        #logging.info(item.courses)
        for c in item.courses:
            c.user = users.query.filter(users.id == c.user_id).first()

    return render_template("index/index.html",username = username,categorys=categorys)
    
@page.errorhandler(404)
@page.route('/error')
def error():
    return render_template('index/error.html'),404

@page.route('/upload/<folder>',methods=['POST'])
def upload_file(folder):
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
            f.save('uploads/{}/{}'.format(folder,newName))
            return '/uploads/{}/{}'.format(folder,newName)
        except Exception,e:
            logging.error(e)
            return ''

@page.route('/cookie/test')
def setCookie():
    resp = make_response(render_template('usercontrol/setting.html',username='username'))
    resp.set_cookie('username', 'username')
    return resp
'''
@page.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
'''
@page.route('/aboutthis')
def about():
    try:
        username = escape(session['username'])
    except:
        username = None

    with open('README.md','rb') as f:
        content = f.read()
        logging.info(content)
        return render_template('about.html',readme=content,username=username)

@page.route('/uploads/<folder>/<filename>',methods=['GET'])
def deliver_file(folder,filename):
    resp = send_file('uploads/{}/{}'.format(folder,filename))
    logging.error(type(resp))
    return resp

@page.route('/category/<int:category_id>',methods=['GET'])
def _category(category_id):
    try:
        page_id = int(request.args.get('pid'))
    except Exception,e:
        logging.warning(e)
        page_id = 1

    category_id = int(category_id)
    current = category.query.filter(category.id == category_id).first()

    items = 10 #控制每页显示课程的数量
    courses = get_courses(page_id, category_id, items)
    count = get_course_count(category_id)

    pageSeq = get_page_seq(count, items)
    #sub_category =category.query.filter(category_to_course.category_id_first == category_id).all()

    return render_template('index/category.html', courses=courses, category=current, pageseq=pageSeq)

@page.route('/course/all',methods = ['GET'])
def get_all_course():
    try:
        page_id = int(request.args.get('pid'))
    except Exception,e:
        logging.warning(e)
        page_id = 1

    items = 10 #控制每页显示课程的数量
    count = get_course_count()
    logging.info(count)
    courses = get_courses(page_id,items = items)

    pageSeq = get_page_seq(count, items)
    logging.info(pageSeq)
    return render_template('index/all_course.html', courses = courses, pageseq = pageSeq)

def get_courses(page_id, category_id=None, items=30):
    if not category_id:
        courses = course.query.filter(course.status==1).order_by(desc(course.create_date)).slice(page_id*items - items, page_id *items).all()

    else:
        courses = course.query.join(category_to_course, category_to_course.course_id == course.id)\
        .filter(category_to_course.category_id_first==category_id,course.status==1).order_by(desc(course.create_date)).slice(page_id*items - items, page_id *items).all()

    logging.info(len(courses))
    return courses

def get_course_count(category_id=None):
    if not category_id:
        count = db_session.query(func.count(course.id)).filter(course.status==1).first()[0]
    else:
        count = db_session.query(func.count(course.id)).join(category_to_course, category_to_course.category_id_first == course.id)\
        .filter(category_to_course.category_id_first==category_id,course.status==1).first()[0]

    logging.info('category id: %s course count: %s', category_id, count)
    return count

@page.route('/menu')
def ul_menu():
    categorys = category.query.filter(category.level == 1).all()
    for item in categorys:
        item.subs = category.query.filter(category.pre_category_id == item.id).all()

    return render_template('index/ul_menu.html',categorys=categorys)

