# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 22:49:29
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from sqlalchemy import Column, Integer,String, Boolean,DateTime
from __init__ import Base
from datetime import datetime

class users(Base):
    """ 用户表 """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) #用户id
    email = Column(String(120), unique=True,index=True) #用户账号，强制使用邮箱
    passward = Column(String(40)) #密码，sha1加密
    new_mail = Column(String(120), unique=True)
    name = Column(String(20),index=True)  #昵称
    level = Column(Integer) #用户权限级别
    gender = Column(String(2)) #性别
    head_pic = Column(String(100))#用户头像
    desc = Column(String(160)) #用户描述
    phone_num = Column(String(13))#电话号码
    qq = Column(String(13))#qq号码
    wechat = Column(String(30))#微信号码
    is_activated = Column(Integer)#更换的邮件是否激活
    verify_code= Column(String(20))#更换邮件的验证码验证码
    note = Column(String(20))#备注
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    def __init__(self, email=None,passward=None,name=None, level=None,gender=0,head_pic=None,\
        desc=None,phone_num=None,qq=None,wechat=None,is_active=None,verify_code=None,note=None,modify_time=None):
        self.name = name
        self.email = email
        self.passward = passward
        self.level = level
        self.gender = gender
        self.head_pic =head_pic
        self.desc = desc
        self.phone_num = phone_num
        self.qq = qq
        self.wechat = wechat
        self.is_active = is_active
        self.verify_code = verify_code
        self.note  = note
        self.create_time = datetime.now()
        self.modify_time =modify_time

    def __repr__(self):
        return '<User %r>' % (self.name)