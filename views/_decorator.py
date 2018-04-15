# -*- coding: utf-8 -*-
# @Date    : 2018-03-06 22:14:55
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from functools import wraps
from flask import request,session,redirect,url_for
from models.users import users
from models.course import course
import logging

#用户登录控制，需要用户登录才能操作的视图，只需要在前面加@login_required
def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            #如果用户已登录，则允许进入点击跳转的页面
            session['email']
            return f(*args, **kwargs)
        except Exception,e:
            logging.error("could not access the url please check! url: %s",request.url)
            logging.error(e)
            #如果用户未登录，则重定向至登录页面
            return redirect(url_for('usercontrol.signin',next=request.url))
    return decorated_func

#用户控制模块，只有用户自己才能操作的模块请添加这个解释器
def self_login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            email = session['email']
            user = users.query.filter(users.email == email).first()
            current_id = request.args.get('id')
            logging.error("email: %s", email)
            logging.error("current_id: %s, request_id: %s", current_id, user.id)
            if int(current_id) == user.id:
                #如果要进入的用户信息页面是当前登录用户的信息页，则允许用户进入，
                return f(*args, **kwargs)
            else:
                #如果要进入的用户信息页面是当前登录用户的信息页，则重定向到用户的基本信息展示页面
                return redirect(url_for('usercontrol.showUser',userid=int(current_id)))
        except Exception,e:
            logging.error(e)
            return redirect(url_for('usercontrol.showUser',userid=int(current_id)))

    return decorated_func

#管理员权限装饰器，控制审核、审核驳回等视图只有管理员才能调用
def admin_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            level = session['level']
            if level == 0:
                #如果是管理员用户，允许进入当前页面
                return f(*args, **kwargs)
            else:
                #如果要进入的用户信息页面是当前登录用户的信息页，则重定向到用户的基本信息展示页面
                return redirect(url_for('index.index'))
        except Exception,e:
            logging.error(e)
            return redirect(url_for('index.index'))

    return decorated_func

#课时管理装饰器，控制用户只能编辑自己课程的课时
def self_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            cid = request.base_url.split('/')[-1]

            email = session['email']
            user = users.query.filter(users.email == email).first()
            c = course.query.filter(course.id == cid).first()

            if c.user_id == user.id:
                #如果是管理员用户，允许进入当前页面
                return f(*args, **kwargs)
            else:
                #如果要进入的用户信息页面是当前登录用户的信息页，则重定向到用户的基本信息展示页面
                return redirect(url_for('resouce_manage.course_manage'))
        except Exception,e:
            logging.error(e)
            return redirect(url_for('resouce_manage.course_manage'))

    return decorated_func