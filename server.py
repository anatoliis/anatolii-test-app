#!/usr/bin/env python
from os import getcwd
from os.path import join

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from jinja2 import Environment, FileSystemLoader
from momoko import Pool

from settings.routes import routes
from settings import DB_PSQL_DSN


define('port', default=8080, help='run on the given port', type=int)
define('debug', default=True, help='debug mode', type=bool)
DIR = getcwd()
STATIC_PATH = join(DIR, 'static')
TEMPLATE_PATH = join(DIR, 'templates')


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path': STATIC_PATH,
            'template_path': TEMPLATE_PATH,
            'login_url': '/login',
            'cookie_secret': '2nWKVDWNR6WhCI/VBeBfscPXpFvJs0LZjdLB7hslv9g=',
            'debug': options.debug,

        }
        tornado.web.Application.__init__(self, routes, **settings)
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

        # PostgreSQL database connection
        ioloop_psql = tornado.ioloop.IOLoop.instance()
        self.db = Pool(dsn=DB_PSQL_DSN, size=1, ioloop=ioloop_psql)
        future_psql = self.db.connect()
        ioloop_psql.add_future(future_psql, lambda f: ioloop_psql.stop())
        ioloop_psql.start()
        future_psql.result()


if __name__ == '__main__':
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
