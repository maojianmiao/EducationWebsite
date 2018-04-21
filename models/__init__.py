# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 22:48:34
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#sqlite数据库路径，最好是绝对路径
database_uri = 'D:/Projects/EducationWebsite/education.db'
engine = create_engine('sqlite:///' + database_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # 在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地
    # 在 metadata 中注册。否则，您将不得不在第一次执行 init_db() 时
    # 先导入他们。
    import recommend
    Base.metadata.create_all(bind=engine)
