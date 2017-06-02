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
        self.render('list.html',length=goods_dict_return['length'], data=goods_dict_return['data'])
        # self.write(goods_dict_return)


# 根据商品名查询所有同名的商品
class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        item = self.get_argument('word')
        goods_dict_return = Base_SQL.Search_function(item)
        self.write(goods_dict_return)


# 根据id 查询商品详情，存在返回details，否则返回{}
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        good_id = self.get_argument('id')
        details = Base_SQL.Detail_functioni(good_id)
        if details != {}:
            price_now = int(details['price']*(100-details['discount'])/100)
            self.render("product-detail.html",id=id,name=details['name'],price=details['price'],price_now=price_now,detail=details['detail'],tag=details['tag'])


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


class CartHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cart.html')
    def post(self):
        #前端发送订单信息。需要验证是否登录
        #格式为{'商品id':数量}
        self.write('1')


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        #验证身份
        user_id = get_secure_cookie('user_id')
        user_dict = Base_SQL.Home_Userinfo_function(user_id)
        order_dict = Home_Orderinfo_function(user_id)
        self.render('home.html',account=user_dict['account'],addr=user_dict['addr'],tel=user_dict['tel'],length=order_dict['length'],data=order_dict['data'])
    def post(self):
        #不支持
        self.write('1')


class PurchaseHandler(tornado.web.RequestHandler):
    def post(self):
         good_id = self.get_argument('good_id')
         good_num = self.get_argument('num')
         user_id = get_secure_cookie('user_id')
         Base_SQL.Purchase_function(good_id, num, user_id)



# 确认支付,根据uuid即order_id
class PurchaseCtrlHandler(tornado.web.RequestHandler):
    def post(self):
         order_id = self.get_argument('uuid')
         Base_SQL.Purchase_Ctrl_function(order_id)


class OrderHandler(tornado.web.RequestHandler):
    def get(self):
         user_id = self.set_secure_cookie('user_id')
         order_dict_return = Base_SQL.Order_function(user_id)
         self.write(order_dict_return)



class AdminHandler(tornado.web.RequestHandler):
    def post(self):
        type=self.get_argument('type')
        id=self.get_argument('id')
        # 这个id在相应情况下是用户号和订单号
        if type=='deluser':
            Base_SQL.Admin_Del_User_function(id)
        elif type=='delorder':
            # 删除订单;result为1,修改成功;为0,则修改失败,result为int
            Base_SQL.Admin_Del_Order_function(order_id)
        elif type=='changeprice':
            # 修改商品价格;result为1,修改成功;为0,则修改失败,result为int
            price=self.get_argument('price')
            result = Base_SQL.Admin_Modify_Price_function(id, price)
        elif type=='changeoff':
            # 修改商品折扣;result为1,修改成功;为0,则修改失败,result为int
            off=self.get_argument('off')
            result = Base_SQL.Admin_Modify_Discount_function(id, off)
    def get(self):
        #验证身份
        #判断请求类型
        try:
            type=self.get_argument('type')
            if type == 'order':
                # 管理员查看所有订单
                Orders = Base_SQL.Admin_Order_function()
                self.write(Orders)
            elif type == 'user':
                # 管理员查看所有用户
                All_users = Base_SQL.Admin_Allusers_function()
                self.write(All_users)
            elif type == 'goods':
                # 管理员查看所有商品
                All_goods = Base_SQL.Admin_AllGoods_function()
        except:
            self.render('admin.html')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", MainHandler),
                                            (r"/off",OffHandler),
                                            (r"/reg", RegHandler),
                                            (r"/detail", DetailHandler),
                                            (r"/login", LoginHandler),
                                            (r"/cart", CartHandler),
                                            (r"/home", HomeHandler),
                                            (r"/list",ListHandler),
                                            (r"/admin", AdminHandler),
                                            ],
                                  static_path=os.path.join(os.path.dirname(__file__), "../static"),
                                  template_path=os.path.join(os.path.dirname(__file__), "../template"),
                                  debug=True,
                                  cookie_secret = "hello")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
