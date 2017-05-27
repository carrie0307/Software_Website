# -*- coding:utf8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import random
import MySQLdb
import Base_SQL
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class OffHandler(tornado.web.RequestHandler):
    def get(self):
        goods_dict_return = Base_SQL.Main_list()
        self.write(goods_dict_return)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index-2.html')
        # goods_dict_return = Base_SQL.Main_list()
        # self.write(goods_dict_return)

class RegHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('user')
        password = self.get_argument('password')
        addr = self.get_argument('addr')
        tel = self.get_argument('tel')
    def get(self):
        self.render('login.html')

# 登录成功返回1,同时写cookie，登录失败返回0
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        id = Base_SQL.Login_function(account, password)
        if id == '0':
            slef.write('0')
        else:
            self.set_secure_cookie('user_id', id)
            self.write('1')
    def get(self):
        self.render('login.html')

# 根据id 查询商品详情，存在返回detail，否则返回str(0)
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        good_id = self.get_argument('id')
        detail = Base_SQL.Detail_functioni(good_id)
        self.write(detail)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", MainHandler),
                                            (r"/off",OffHandler),
                                            (r"/reg", RegHandler),
                                            (r"/login", LoginHandler)],
                                  static_path=os.path.join(os.path.dirname(__file__), "../static"),
                                  template_path=os.path.join(os.path.dirname(__file__), "../template"),
                                  debug=True,
                                  cookie_secret = "hello")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
