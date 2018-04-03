# -*- coding: utf-8 -*-
# @Date    : 2018-03-22 22:01:05
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from users import users
from course import course
from datetime import datetime
from __init__ import Base

class course_rate(Base):
    __tablename__ = 'course_rate'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    create_date  = Column(DateTime)
    users = relationship("users")
    course = relationship("course")

    def __init__(self, score=None, comment=None, user_id=None, course_id=None, user=None, course=None):
        self.score = score
        self.comment = comment
        self.create_date = datetime.now()
        if user_id:
            self.user_id = user_id
        else:
            self.users = user
        
        if course_id:
            self.course_id = course_id
        else:
            self.course = course

    def __repr__(self):
        return "<score: %s>" % self.score


