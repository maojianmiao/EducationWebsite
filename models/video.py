# -*- coding: utf-8 -*-
# @Date    : 2018-03-02 23:31:00
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from course import course
from __init__ import Base
from datetime import datetime

class video(Base):
    """ 单个课时视频表 """
    __tablename__ = 'video'

    id = Column(Integer,primary_key=True)
    title = Column(String(40))
    order = Column(Integer)
    video_url = Column(String(150))
    description = Column(Text)
    view = Column(Text)
    course_id = Column(Integer,ForeignKey('course.id'))
    course = relationship('course')
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    duration = Column(Float)

    def __init__(self,title,video_url,order=1,course_id=None,description=None,view=0,modify_date=None,course=None,duration=1):
        self.title = title
        self.order = order
        self.video_url = video_url
        
        if course_id:
            self.course_id = course_id
        else:
            self.course = course
            
        self.description = description
        self.view = view
        self.create_date = datetime.now()
        self.modify_date = modify_date
        self.duration = duration