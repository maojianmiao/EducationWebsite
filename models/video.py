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
    status = Column(Integer)##课程状态0: 未审核；1：已审核；2：审核中 3：已修改 4:审核驳回 5:删除中 6: 已删除
    audit_by = Column(String(24))
    audit_note = Column(String(100))

    def __init__(self,title=None,video_url=None,order=1,course_id=None,description=None,view=0,modify_date=None,course=None,duration=1,status=0,audit_by=None,audit_note=None):
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
        self.status = status
        self.audit_by = audit_by
        self.audit_note = audit_note

    def get_status_text(self):
        status_dict = {0:u'未审核', 1:u'审核通过',2:u'审核中',3:u'已修改',4:u'审核驳回',
                        5:u'删除',6:'已删除',}
        try:
            return status_dict[int(self.status)]
        except Exception,e:
            logging.error(e)
            return u'未知的'
    def __repr__(self):
        return "<title: %s >" % self.title