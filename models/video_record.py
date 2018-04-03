# -*- coding: utf-8 -*-
# @Date    : 2018-03-03 10:30:17
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from users import users
from course import course
from video import video
from datetime import datetime
from __init__ import Base

class video_record(Base):
    """用户课时进度表"""
    __tablename__ = 'video_record'

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    video_id = Column(Integer, ForeignKey('video.id'))
    play_time = Column(Float)
    is_finished = Column(String(1)) #0:未完成 1：完成
    users =relationship(users)
    course = relationship(course)
    video = relationship(video)
    create_time = Column(DateTime)

    def __init__(self,user_id=None,course_id=None,video_id=None,play_time=None,is_finished='0',\
        users=None,course=None,video=None):
        self.play_time = play_time
        self.is_finished = is_finished
        self.create_time = datetime.now()
        if user_id:
            self.user_id = user_id
        else:
            self.users = users
        if course_id:
            self.course_id = course_id
        else:
            self.course = course
        if video_id:
            self.video_id = video_id
        else:
            self.video = video
    
    def __repr__(self):
        print('<play_time %s>' % self.play_time)