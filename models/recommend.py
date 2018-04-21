# -*- coding: utf-8 -*-
# @Date    : 2018-04-21 13:36:47
# @Author  : linyuling
# @Version : $Id$
# @Notes   : 


from sqlalchemy import Column, Integer,String,Text,ForeignKey
from __init__ import Base

class recommend(Base):
    """精品推荐内容"""
    __tablename__ = 'recommend'

    id = Column(Integer,primary_key=True)
    title = Column(String(100))
    link = Column(String(200))
    src = Column(String(200))
    desc = Column(Text)

    def __init__(self, title=None,link=None,desc=None,src=None):
        self.title = title
        self.link = link
        self.desc = desc
        self.src = src

    def __repr__(self):
        return '<recommend id:%s>' % self.id

