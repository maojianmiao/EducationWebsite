# -*- coding: utf-8 -*-
# @Date    : 2018-02-28 22:23:02
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from users import users
from __init__ import Base
from datetime import datetime

class course(Base):
    """ 课程系列表 """
    __tablename__ = 'course'


    id = Column(Integer,primary_key=True)
    title = Column(String(40),index=True) #课程名，添加索引，增加检索效率
    user_id = Column(Integer,ForeignKey('users.id')) #上传者id
    users = relationship("users") #用户
    view = Column(Integer,index=True) #查看数，添加索引，增加检索效率
    score = Column(Float) #评分，满分10分
    score_count = Column(Integer) #评分人数
    description = Column(Text) #描述
    cost = Column(Float) #学习课程费用，0表示免费
    item_image = Column(String(100))#小缩略图
    status = Column(Integer)##课程状态0: 未审核；1：已审核；2：审核中 3：已修改 4:审核驳回 5:删除 6: 已删除
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    
    audit_by = Column(String(24))
    audit_note = Column(String(100))

    def __init__(self,title=None, view=0,score=0,score_count=0,description=None,cost=None,\
        item_image=None,modify_date=None,user_id=None,users=None,status=0,audit_by=None,audit_note=None):
        
        self.title = title
        self.view = view
        self.score = score
        self.score_count = score_count
        self.description = description
        self.cost = cost
        self.item_image = item_image
        self.modify_date = modify_date
        self.create_date = datetime.now()
        if user_id:
            self.user_id = user_id
        else:
            self.users = users
            
        self.status = status
        self.audit_by = audit_by
        self.audit_note = audit_note

    def get_status_text(self):
        status_dict = {0:u'未审核', 1:u'审核通过',2:u'审核中',3:u'已修改',4:u'审核驳回',
                        5:u'删除',6:'已删除',
                            }
        return status_dict[self.status]

    def __repr__(self):
        return u'<title %s>' % self.title

"""
class course_temp(Base):
 
    __tablename__ = 'course_temp'

    id = Column(Integer,primary_key=True)
    title = Column(String(40),index=True) #课程名，添加索引，增加检索效率
    user_id = Column(Integer,ForeignKey('users.id')) #上传者id
    users = relationship("users") #用户
    view = Column(Integer,index=True) #查看数，添加索引，增加检索效率
    score = Column(Float) #评分，满分10分
    score_count = Column(Integer) #评分人数
    description = Column(Text) #描述
    cost = Column(Float) #学习课程费用，0表示免费
    item_image = Column(String(50))#小缩略图
    status = Column(String(50))#大缩略图
    create_date = Column(DateTime)
    modify_date = Column(DateTime)
    status = Column(String(1)) #课程状态0: 未审核；1：审核中；2：已审核 3：已审核-编辑 
    audit_by = Column(String(24))
    note = Column(String(100))

    def __init__(self,title=None, view=0,score=0,score_count=0,description=None,cost=None,\
        item_image=None,detail_image=None,modify_date=None,user_id=None,users=None,status=0, audit_by="admin",note=None):
        
        self.title = title
        self.view = view
        self.score = score
        self.score_count = score_count
        self.description = description
        self.cost = cost
        self.item_image = item_image
        self.status = detail_image
        self.modify_date = modify_date
        self.create_date = datetime.now()
        if user_id:
            self.user_id = user_id
        else:
            self.users = users
        self.status = status
        self.audit_by = audit_by
        self.note = note

    def __repr__(self):
        return u'<title %s>' % self.title

class temp_to_course(Base):
    
    __tablename__ = 'temp_to_course'

    id = Column(Integer, primary_key=True)
    course_temp_id = Column(Integer, ForeignKey('course_temp.id'))
    course_id = Column(Integer,ForeignKey('course.id'))

    course_temp = relationship('course_temp')
    course = relationship('course')

    def __init__(self, course_temp_id=None, course_id=course_id,course_temp=None,course=None):
        if course_id:
            self.course_id = course_id
        else:
            self.course = course

        if course_temp_id:
            self.course_temp_id
        else:
            self.course_temp

    def __repr__(self):
        return '<course_temp id: %s>' % self.course_temp_id

"""