# -*- coding: utf-8 -*-
# @Date    : 2018-02-12 18:58:47
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from flask import Flask,url_for,request,render_template, make_response,abort,redirect,session,escape\
,flash,Blueprint,g
from common.api import hash_string,get_random_texts,to_dict
from common.sitemail import sitemail
from common.security import encrypt_string,decrypt_string
from models.users import users
from models.course import course
from models.user_to_course import user_to_course,collect
from models.change_email import change_email
from models.jitang import jitang
from models.__init__ import db_session
from sqlalchemy import asc,desc
from _decorator import login_required,self_login_required
import logging
import random
import re

page = Blueprint('usercontrol',__name__)

@page.route('/signin',methods=['POST','GET'])
def signin():
    #检查缓存，如果有直接走缓存的设置
    if 'username' in  session:
        return redirect(url_for("index.index"))

    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')

        current = users.query.filter_by(email=username).first()
        if not current:
            return render_template('usercontrol/login.html',msg="账号不存在，请重新输入！")


        if username == current.email and hash_string(passwd) == current.passward:
            session['username'] = current.name
            session['email'] = username
            session['userid'] = current.id
            session['head_pic'] = current.head_pic
            return redirect(url_for("index.index"))
        else:
            return render_template('usercontrol/login.html',msg="输入的账号或密码不正确！")

    return render_template('usercontrol/login.html',msg='') 

@page.route('/signup',methods=['POST','GET'])
def signup():
    if 'username' in  session:
        return redirect(url_for("index.index"))
    
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        passwd2 = request.form.get('passwd2')
        auth_code = request.form.get('input_auth_code')

        current = users.query.filter_by(email=username).first()
        if current:
            return render_template('usercontrol/signup.html',msg="该邮箱已被注册，请重新输入！")
        
        if passwd != passwd2:
            return render_template('usercontrol/signup.html',msg="两次输入的密码不相同！")
        #创建一个用户数据类

        try:
            code = escape(session[username])
        except:
            code = 'fakecode'
            
        if auth_code != code:
            return render_template('usercontrol/signup.html',msg="验证码错误！")
        #默认昵称为邮箱名去掉@xxx.com
        default_name = username.split('@')[0]
        #默认头像图片
        default_pic = '/static/images/defaultpic.jpg'
        new = users(username, hash_string(passwd),name=default_name,head_pic=default_pic)
        #提交到数据库
        db_session.add(new)
        db_session.commit()
        session['username'] = default_name
        session['email'] = username
        session['userid'] = new.id
        logging.info(new.id)
        return redirect(url_for("index.index"))

    return render_template('usercontrol/signup.html',msg='')

@page.route('/logout')
@login_required
def logout():
    try:
        session.pop('username', None)
        session.pop('head_pic', None)
        session.pop('email', None)
        return redirect(url_for("usercontrol.signin"))
    except Exception,e:
        logging.error(e)
        return 'Something wrong'

@page.route('/auth_code',methods=['GET'])
def get_auth_code():
    confirm = getattr(g,'mail_server',None)
    if not confirm:
        mail_server = sitemail()
        mail_server.mail_server()
        g.mail_server = mail_server

    if request.method =='GET':
        mail_to = request.args.get('username')
        title = '代号010教育网站注册验证码'
        code = get_random_texts(5)
        content = '欢迎注册代号010教育网站，你的验证码为:{}'.format(code)

        status = g.mail_server.send(mail_to,title, content)
        if status:
            #在浏览器写一个key为邮箱，值为验证码的session
            #后面验证直接用session
            session[mail_to] = code
            logging.info(escape(session[mail_to]))
            return hash_string(code)


@page.route('/setting',methods=['GET','POST'])
@login_required
@self_login_required
def setting():
    setting_dict = {}
    setting_dict['displayStyle'] = ''  #为id=sendMai的p标签设置样式
    # 进入的连接域名必须为 /setting?id=1
    userid = int(request.args.get('id'))
    current = users.query.filter(users.id==userid).first()
    #筛选出id号最大的
    email = change_email.query.filter(change_email.users_id==userid,change_email.is_available=='1').order_by(desc(change_email.id)).first()
    #修改邮件后，已发送激活链接，新设置的邮件处于待激活状态
    if email and email.verification_code:
        setting_dict['displayStyle'] = "background-color:gray"
        setting_dict['btnText'] = u"登录邮箱验证"
        setting_dict['settingEmail'] = email.email
        setting_dict['emailMsg'] = '请验证邮箱。如已验证，请刷新页面'
    if email and not email.verification_code:
        setting_dict['btnText'] = u"发送验证邮件"
        setting_dict['settingEmail'] = email.email
        setting_dict['emailMsg'] = u'邮箱为网站唯一登录账号，非常重要'
    if not email:
        setting_dict['displayStyle'] = "display:none"
        session['email'] = current.email
        setting_dict['settingEmail'] = current.email
        setting_dict['emailMsg'] = u'邮箱为网站唯一登录账号，非常重要'

    #用户性别信息设置
    if str(current.gender) == '0':
        setting_dict['privacy_checked'] = 'checked'
    if str(current.gender) == '1':
        setting_dict['male_checked'] = 'checked'
    if str(current.gender) == '2':
        setting_dict['female_checked'] = 'checked'

    #需要从数据库获取值得设置项，全部写入字典，传给前端
    items = ['head_pic','gender','phone_num','wechat','qq','desc','name','id']
    for item in items:
        if getattr(current,item):
            setting_dict[item] = getattr(current,item)

    logging.info(setting_dict)
    return render_template('usercontrol/setting.html',**setting_dict)

#更新设置修改的数据到数据库
@page.route('/updateinfo',methods=['POST'])
def update_info():
    logging.info(request.form)
    current = users.query.filter(users.id==session["userid"]).first()
    try:
        for key,value in request.form.items():
            #设置current对象的属性值
            if key == 'head_pic':
                #把图片的地址换成相对路径
                root_url = re.match('http(s|)://[^/]*',value).group()
                value = value.replace(root_url,'')
            setattr(current,key,value)
        db_session.commit()
        session['username'] = request.form.get('name')
        session['head_pic'] = current.head_pic
        logging.info('head_pic:',current.head_pic)
        return 'success'
    except Exception,e:
        logging.error(e)
        return ''

@page.route('/newemail/store',methods=['GET'])
@login_required
def store_email():
    if request.method == 'GET':
        try:
            userid = request.args.get('userid')
        except:
            userid = session['userid']
        newEmail = request.args.get('newEmail')

        old_emails = change_email.query.filter(change_email.users_id==int(userid)).all()
        if old_emails:
            for email in old_emails:
                email.is_available = '0'

        change = change_email(email=newEmail,users_id=int(userid))
        db_session.add(change)
        try:
            db_session.commit()
            return 'success'
        except Exception,e:
            logging.error(e)
            return ''


@page.route('/newemail/send',methods=['GET','POST'])
@login_required
def send_email():
    if request.method == 'GET':
        try:
            userid = request.args.get('userid')
        except:
            userid = session['userid']
        newEmail = request.args.get('newEmail')
        
        change = change_email.query.filter(change_email.users_id==int(userid),change_email.email==newEmail,change_email.is_available=="1").first()
        if not change:
            logging.error("could not find valid data in table")
            return 'fail'

        verification_code = get_random_texts(5)
        activate_string = encrypt_string('email={}&userid={}&vc={}&changeid={}'.format(newEmail,userid,verification_code,change.id))
        logging.info(activate_string)

        
        
        change.verification_code = verification_code
        db_session.commit()

        activate_url = '{}activate?code={}'.format(request.url_root,activate_string)
        logging.info(activate_url)

        confirm = getattr(g,'mail_server',None)
        if not confirm:
            mail_server = sitemail()
            mail_server.mail_server()
            g.mail_server = mail_server
        #发送带激活链接的邮件到用户邮箱
        mail_to = newEmail
        title = '代号010教育网站邮箱更换激活链接'
        content = '请点击以下链接，激活新邮件:\r\n{}'.format(activate_url)
        try:
            status = g.mail_server.send(mail_to,title, content)
            return 'success'
        except Exception,e:
            logging.error(e)
            return ''
#通过链接激活邮件
@page.route('/activate')
def activate():
    string = request.args.get('code')
    params = decrypt_string(string.encode('utf-8'))

    d = to_dict(params)
    logging.info(d)

    user = users.query.filter_by(id=int(d['userid'])).first()
    change = change_email.query.filter_by(id=int(d['changeid'])).first()
    if change.is_activated == '1':
        return render_template('usercontrol/notice.html',msg=u'邮箱已激活！')
    #修改用户主表的登录邮箱账号
    session['email'] = d['email']
    user.email = d['email']
    #邮箱激活后，把change_email表的数据处理下
    change.is_available = '0' #废弃这条数据
    change.is_activated = '1' #表示这个邮箱已经激活了
    db_session.commit()
    return render_template('usercontrol/notice.html',msg=u'邮箱已激活！')

@page.route('/user/<userid>')
@login_required
def showUser(userid):
    user = users.query.filter(users.id == int(userid)).first()
    return render_template('usercontrol/user.html',user=user,setting='/setting?id={}'.format(userid))


@page.route('/course/record')
@login_required
def course_record():

    email = session['email']
    user = users.query.filter(users.email == email).first()

    courses = course.query.join(user_to_course, course.id == user_to_course.course_id).\
    filter(user_to_course.user_id == user.id).all()

    jitangs = jitang.query.filter().all()
    select_jitang = random.choice(jitangs)
    title = u'我的学习'

    return render_template('usercontrol/course_record.html',courses=courses, jitang=select_jitang, title=title)

@page.route('/course/collect/add', methods=['POST'])
@login_required
def add_collect():
    email = session['email']
    user = users.query.filter(users.email == email).first()

    course_id = int(request.form.get('course_id'))

    confirm = collect.query.filter(collect.user_id == user.id, collect.course_id == course_id).first()
    if confirm:
        return 'success'

    try:
        new_collect = collect(user_id = user.id, course_id = course_id)
        db_session.add(new_collect)
        db_session.commit()
        return 'success'
    except Exception,e:
        logging.error(e)
        return 'failed'

@page.route('/course/collect/cancel', methods=['POST'])
@login_required
def delete_collect():
    email = session['email']
    user = users.query.filter(users.email == email).first()

    course_id = int(request.form.get('course_id'))

    confirm = collect.query.filter(collect.user_id == user.id, collect.course_id == course_id).first()
    if not confirm:
        return 'success'

    try:
        db_session.delete(confirm)
        db_session.commit()
        return 'success'
    except Exception,e:
        logging.error(e)
        return 'failed'


@page.route('/course/record/collect')
@login_required
def get_collect():
    email = session['email']
    user = users.query.filter(users.email == email).first()

    courses = course.query.join(collect, course.id == collect.course_id).filter(collect.user_id == user.id).all()

    jitangs = jitang.query.filter().all()
    select_jitang = random.choice(jitangs)
    title = u'我的收藏'

    return render_template('usercontrol/course_record.html',courses=courses, jitang=select_jitang, title=title)

@page.route('/email/check')
def check_mail():

    email = request.args.get('email')
    try:
        current = escape(session['email'])
    except:
        current = None

    confirm = users.query.filter(users.email == email,users.email != current).first()
    if confirm:
        return 'invalid'
    else:
        return 'valid'