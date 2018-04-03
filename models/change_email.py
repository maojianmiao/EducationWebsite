# -*- coding: utf-8 -*-
# @Date    : 2018-02-20 12:58:33
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from __init__ import Base
from users import users
from datetime import datetime

class change_email(Base):
    ''' 用户需要修改绑定邮箱时所用的表，保存未激活但保存了的邮箱'''
    __tablename__ = 'change_email'

    id = Column(Integer, primary_key=True)
    email = Column(String(100),index=True)
    is_activated = Column(String(1))
    verification_code = Column(String(12))
    users_id = Column(Integer,ForeignKey('users.id'))
    users = relationship('users')
    create_time = Column(DateTime)
    activate_time = Column(DateTime) 
    is_available = Column(String(2)) #1:available; 0:not available

    def __init__(self,users=None,email=None,is_activated=0,verification_code=None,activate_time=None,is_available='1',users_id=None):
        self.email = email
        self.is_activated = is_activated
        self.verification_code = verification_code
        #self.users = users
        self.create_time = datetime.now()
        self.activate_time = activate_time
        self.is_available = is_available
        if users_id:
            self.users_id = users_id
        else:
            self.users = users
        
    def _repr__(self):
        return "<change_email %s>" % self.email

