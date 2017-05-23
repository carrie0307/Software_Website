# -*- coding:utf8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import random
# import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def post(self):

        pass

    def get(self):
        # self.render('xixi.html', state="")
        phone = self.get_argument('type')
        self.write(phone)
        # phone = self.get_argument('type')
        # print phone
        #self.write(self.request.headers['user-agent'] +\
			#"\nyour current ip is: "+self.request.remote_ip)

        #posturl="index.html"
        # self.render("")


class SearchHandler(tornado.web.RequestHandler):
    #更换种子
    def post(self):
        user = self.get_argument('user')
        sqlstr = "SELECT password FROM user WHERE user='%s'" % user
        cur.execute(sqlstr)
        password = cur.fetchone()[0]
        seed = random.randint(1,0xFFFFFFFF-1)
        last = hashlib.md5(str(password | seed)).hexdigest()
        #last = str((int(last)/0xFFFF)^(int(last)%0xFFFF))
        for i in range(0,10):
            last = hashlib.md5(last).hexdigest()
        #last = hashlib.md5((last_t/0xFFFF)^(last_t%0xFFFF))
        sqlstr = "UPDATE user SET seed = %d, lastkey = '%s' WHERE user='%s'" % (seed, last, user)
        cur.execute(sqlstr)
        conn.commit()
        self.write(str(seed))
        with open('Log.txt','a+') as f:
            f.write('Change Seed:%s\n'%user)
            f.close()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/xixi.html", MainHandler),],
                                  static_path=os.path.join(os.path.dirname(__file__), "static"),
                                  template_path=os.path.join(os.path.dirname(__file__), "template"),
                                  debug=True)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
