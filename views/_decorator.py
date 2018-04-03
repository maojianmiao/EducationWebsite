# -*- coding: utf-8 -*-
# @Date    : 2018-03-06 22:14:55
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from functools import wraps
from flask import request,session,redirect,url_for
from models.users import users
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

