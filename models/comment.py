# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 01:29:44
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

class comment(Base):
    """用户评论表"""

    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(Text)  #评论内容
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False) #添加评论的用户id
    course_id = Column(Integer,ForeignKey('course.id'))
    video_id = Column(Integer,ForeignKey('video.id'))
    create_date = Column(DateTime) #创建日期
    like = Column(Integer) #喜欢，赞同
    dislike = Column(Integer) #不喜欢，不赞同
    level = Column(Integer) #评论级别
    view = Column(Integer) #查看数
    create_date = Column(DateTime)
    users = relationship('users')
    course = relationship('course')
    video = relationship('video')

    def __init__(self, user_id=None,course_id=None,video_id=None,comment=None,like=0,level=None,view=0,users=None,course=None,video=None):
        self.comment = comment
        self.create_date = datetime.now()
        self.like = like
        self.level = level
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
        
        
        

    def __repr__(self):
        return '<comment %s>' % self.comment
