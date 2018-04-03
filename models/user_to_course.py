# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 20:51:11
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from users import users
from course import course
from datetime import datetime
from __init__ import Base

class user_to_course(Base):
    """用户学习课程记录 """
    __tablename__ = 'user_to_course'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer,ForeignKey('course.id'))
    users = relationship('users')
    course = relationship('course')
    def __init__(self, user_id=None, course_id=None,users=None, course=None):
        if user_id:
            self.user_id = user_id
        else:
            self.users = users
        if course_id:
            self.course_id = course_id
        else:
            self.course = course
    def __repr__(self):
        return '<user id: %s course id: %s>' % (self.user_id,  self.course_id)


class collect(Base):

    ''' 用户收藏课程记录 '''
    __tablename__ = 'collect'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer,ForeignKey('course.id'))
    users = relationship('users')
    course = relationship('course')

    def __init__(self, user_id=None, course_id=None,users=None, course=None):
        if user_id:
            self.user_id = user_id
        else:
            self.users = users
        if course_id:
            self.course_id = course_id
        else:
            self.course = course
    def __repr__(self):
        return '<user id: %s course id: %s>' % (self.user_id,  self.course_id)
