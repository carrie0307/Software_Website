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


# 根据商品类别查询所有同名的商品
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        ttype = self.get_argument('type')
        goods_dict_return = Base_SQL.List_function(ttype)
        self.write(goods_dict_return)


# 根据商品名查询所有同名的商品
class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        item = self.get_argument('word')
        goods_dict_return = Base_SQL.Search_function(item)
        self.write(goods_dict_return)


# 根据id 查询商品详情，存在返回detail，否则返回str(0)
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        good_id = self.get_argument('id')
        detail = Base_SQL.Detail_functioni(good_id)
        self.render("detail.html",detail=detail)


# 登录成功返回1,同时写cookie，登录失败返回0
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        user_id = Base_SQL.Login_function(account, password)
        if id == '000':
            self.write('0')
        else:
            self.set_secure_cookie('user_id', user_id)
            self.write('1')
    def get(self):
        self.render('login.html')

                        
class RegHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        addr = self.get_argument('addr')
        tel = self.get_argument('tel')
        user_id = Base_SQL.Reg_function(account, password, addr, tel)
        if user_id == '000':
            self.write('0')
        else:
            self.set_secure_cookie('user_id', user_id)
            self.write('1')
    def get(self):
        self.render('login.html')

# 购物车怎么写
class CartHandler(tornado.web.RequestHandler):
    def get(self):
         pass
         # 购物车怎么写


class PurchaseHandler(tornado.web.RequestHandler):
    def get(self):
         pass
         # 下订单;statue的状态是针对具体某个商品还是全部？


class PurchaseCtrlHandler(tornado.web.RequestHandler):
    def get(self):
         pass
         # 拿到了userid，如何确定是哪一个订单？


class OrderHandler(tornado.web.RequestHandler):
    def get(self):
         user_id = self.set_secure_cookie('user_id')
         order_dict_return = Base_SQL.Order_function(user_id)
         self.write(order_dict_return)


# 管理员查看所有订单
class Admin_Orders_Handler(tornado.web.RequestHandler):
    def get(self):
         Base_SQL.Admin_Order_function()


class Admin_Allusers_Handler(tornado.web.RequestHandler):
    def get(self):
         Base_SQL.Admin_Order_function()





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
