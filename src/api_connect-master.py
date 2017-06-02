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
        ttype=self.get_argument('type')
        dict={'length':6,'data': { '1': ['AIPC笔记本电脑', 600, 75], '2': ['小米√3', 600, 75], '3': ['锁尼兰牙耳机', 600, 75], '4': ['基械键盘', 600, 75], '5': ['金是顿U盘', 600, 75], '6': ['平果MP3', 600, 75] }}

        self.render('list.html',length=dict['length'], data=dict['data'])
        '''
        ttype = self.get_argument('type')
        goods_dict_return = Base_SQL.Search_function(ttype)
        self.write(goods_dict_return)
        '''


# 根据商品名查询所有同名的商品
class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        item = self.get_argument('word')
        goods_dict_return = Base_SQL.Search_function(item)
        self.write(goods_dict_return)


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
        account='江泽民'
        addr='北京301医院'
        tel='110'
        length=3
        data={'1111111111':{'uid':'1','id':1,'name':'乐死手机','num':5,'sum':5555,'time':'2017-05-05 23:59:59','statue':0},'1111111112':{'uid':'1','id':2,'name':'乐死炸弹','num':1,'sum':555,'time':'2017-05-05 23:59:59','statue':1},'1111111113':{'uid':'1','id':3,'name':'乐死挖掘机','num':2,'sum':66666,'time':'2017-05-05 23:59:59','statue':0}}
        self.render('home.html',account=account,addr=addr,tel=tel,length=length,data=data)

    def post(self):
        #不支持
        self.write('1')


# 根据id 查询商品详情，存在返回detail，否则返回str(0)
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        good_id = self.get_argument('id')
        #detail = Base_SQL.Detail_functioni(good_id)
        id='2'
        name='华萎手机'
        detail='荣耀X1[2]  采用Kirin 910 1.6GHz四核处理器、2GB内存+16GB储存空间、7英寸1824x1200分辨率屏幕、1300万+前置500万像素摄像头、5000mAh容量电池；[3-4] '
        price=666
        off=75
        tag='手机'
        price_now=int(price*(100-off)/100)
        self.render("product-detail.html",id=id,name=name,price=price,price_now=price_now,detail=detail,tag=tag)


# 登录成功返回1,同时写cookie，登录失败返回0
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        id = Base_SQL.Login_function(account, password)
        if id == '0':
            self.write('0')
        else:
            self.set_secure_cookie('user_id', id)
            self.write('1')
    def get(self):
        self.render('login.html')

                        
class RegHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        addr = self.get_argument('addr')
        tel = self.get_argument('tel')
        print password
    def get(self):
        self.render('login.html')

class AdminHandler(tornado.web.RequestHandler):
    def post(self):
        type=self.get_argument('type')
        id=self.get_argument('id')
        if type=='deluser':
            pass#删除用户
        elif type=='delorder':
            pass#删除订单
        elif type=='changeprice':
            price=self.get_argument('price')
            pass#改价格
        elif type=='changeoff':
            off=self.get_argument('off')
            pass#改折扣
    def get(self):
        #验证身份
        #判断请求类型
        try:
            type=self.get_argument('type')
            if type == 'order':
                self.write({'length':3,'data':{'1111111111':{'uid':'1','id':1,'name':'乐死手机','num':5,'sum':5555,'time':'2017-05-05 23:59:59','statue':0},'1111111112':{'uid':'1','id':2,'name':'乐死炸弹','num':1,'sum':555,'time':'2017-05-05 23:59:59','statue':1},'1111111113':{'uid':'1','id':3,'name':'乐死挖掘机','num':2,'sum':66666,'time':'2017-05-05 23:59:59','statue':0}}})
            elif type == 'user':
                self.write({'length':3,'data':{'1':{'account':'乐','addr':'hit','tel':'110'},'2':{'account':'乐2','addr':'hit','tel':'110'},'3':{'account':'乐3','addr':'hit','tel':'110'}}})
            elif type == 'goods':
                self.write({'length':3,'data':{'1':{'name':'乐死手机','type':'手机','price':5555,'off':75},'2':{'name':'乐死手机','type':'手机','price':5555,'off':75},'3':{'name':'乐死手机','type':'手机','price':5555,'off':75}}})
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
