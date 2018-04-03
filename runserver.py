# -*- coding: utf-8 -*-
# @Date    : 2018-02-12 19:21:08
# @Author  : linyuling
# @Version : $Id$
# @Notes   :

from flask import Flask,render_template,g
from views.usercontrol import page as usercontrol
from views.index import page as index
from models import db_session
from models.users import users
from views.test_view import page as test
from common.sitemail import sitemail
from views.search import page as search
from views.videoplayer import page as videoplayer
from views.resource_manage import page as resource_manage
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging

app = Flask(__name__)
app.config.from_object('config')
#注册views下的所有蓝图
app.register_blueprint(usercontrol)
app.register_blueprint(index)
app.register_blueprint(test)
app.register_blueprint(search)
app.register_blueprint(videoplayer)
app.register_blueprint(resource_manage)
#每次结束请求后关闭数据库连接
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s: %(message)s",datefmt="%m/%d/%Y %p %I:%M:%S")
    #app.logger.info(app.config)
    app.run(port=5000)
