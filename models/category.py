# -*- coding: utf-8 -*-
# @Date    : 2018-03-15 23:32:57
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from sqlalchemy import Column, Integer,String, Boolean,Text,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from course import course
from __init__ import Base
from datetime import datetime

#分类表
class category(Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key=True)
    category_name = Column(String(14),index=True, primary_key=True) #分类名
    level = Column(Integer)#分类级别：1、2、3、4
    views = Column(Integer) #频道vv统计
    pre_category_id = Column(Integer) #上级标签id
    page_pic = Column(String(200))#进入当前分类页面时显示顶部大图图片地址

    def __init__(self,category_name=None, level=None,views=0,pre_category_id=None):
        self.category_name = category_name
        self.level = level
        self.views = views
        self.pre_category_id = pre_category_id

    def __repr__(self):
        return '<category_name:%s>' % self.category_name

#分类栏目与课程关联表
class category_to_course(Base):
    __tablename__ = 'category_to_course'
    id = Column(Integer,primary_key=True)
    course_id = Column(Integer,ForeignKey('course.id'),index=True)
    category_id_first = Column(Integer,index=True)
    category_id_second = Column(Integer,index=True)
    category_id_third = Column(Integer,index=True)
    category_id_fouth = Column(Integer,index=True)
    course = relationship('course')

    def __init__(self,course_id=None, category_id_first=None, category_id_second=None, category_id_third=None,category_id_fouth=None, course=None):
        if course_id:
            self.course_id = course_id
        else:
            self.course = course
        self.category_id_first = category_id_first
        self.category_id_second = category_id_second
        self.category_id_third = category_id_third
        self.category_id_fouth = category_id_fouth

    def __repr__(self):
        return '<category_id:%s --- course_id:%s >' %(self.category_id_first, self.course_id)
