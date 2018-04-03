# -*- coding: utf-8 -*-
# @Date    : 2018-01-28 17:27:14
# @Author  : linyuling
# @Version : $Id$
# @Notes   :


from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from runserver import app

print("start server...")
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()