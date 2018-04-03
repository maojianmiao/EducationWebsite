# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 23:10:56
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from sqlalchemy import Column, Integer,String, Text,DateTime
from __init__ import Base
from datetime import datetime

class jitang(Base):
    """心灵鸡汤，暖身"""
    __tablename__ = 'jitang'

    id = Column(Integer,primary_key=True)
    content = Column(Text) #鸡汤正文
    author = Column(String(20))#鸡汤作者
    create_date = Column(DateTime)
    def __init__(self, content=None,author=None):
        self.content = content
        self.author = author
        self.create_date = datetime.now()

    def __repr__(self):
        return '<content: %s>' % self.content