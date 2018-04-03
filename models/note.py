# -*- coding: utf-8 -*-
# @Date    : 2018-03-07 22:09:38
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

class note(Base):
    __tablename__ = "note"

    id = Column(Integer,primary_key=True)
    note = Column(Text)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False) #添加笔记的用户id
    course_id = Column(Integer,ForeignKey('course.id'))
    video_id = Column(Integer,ForeignKey('video.id'))
    video_position = Column(String(8))
    create_date = Column(DateTime) #创建日期
    like = Column(Integer) #喜欢，赞同
    dislike = Column(Integer) #不喜欢，不赞同
    level = Column(Integer) #
    view = Column(Integer) #
    users = relationship('users')
    course = relationship('course')
    video = relationship('video')

    def __init__(self, note, video_position=None,user_id=None,course_id=None,video_id=None,like=0,view=0,users=None,course=None,video=None):
        self.like = like
        self.note = note
        self.video_position = video_position
        self.view = view
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
        self.create_date  = datetime.now()

    def __repr__(self):
        return '<note %s>' % self.note