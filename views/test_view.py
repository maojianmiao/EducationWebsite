# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 23:38:31
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts
from common.sitemail import sitemail
from models.users import users
from models import db_session
import logging

page = Blueprint('test',__name__)

@page.route('/test',methods=['POST'])
def testRequest():
    if request.method == 'POST':
        logging.info('nick name is: %s',request.values.get('username'))
        logging.info(request.values)
        logging.info(request.headers)
        #logging.info(request.environ)
        return 'success'

@page.route('/notice',methods=['GET'])
def notice():
    return render_template('usercontrol/notice.html',msg="已经登录")