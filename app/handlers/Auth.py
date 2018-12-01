import re
import tornado.gen

from tornado.escape import xhtml_escape
from psycopg2.extras import RealDictCursor
from psycopg2 import IntegrityError

from app.handlers import BaseHandler
from app.sql_methods.users import create_user, get_user_info


class Signin(BaseHandler):
    def prepare(self):
        return None

    @tornado.gen.coroutine
    def get(self):
        if self.get_current_user() is not None:
            self.redirect('/')
        else:
            self.render('signin.html')

    @tornado.gen.coroutine
    def post(self):
        login = xhtml_escape(self.get_argument('login'))
        password = xhtml_escape(self.get_argument('password'))

        cursor_user = yield self.db.execute(get_user_info(login), cursor_factory=RealDictCursor)
        user = cursor_user.fetchall()
        if not user or user[0]['passw'] != password:
            self.render('signin.html',
                        message = '<div class="alert alert-danger" role="alert">' \
                                  'Incorrect login or password<br>Please try again</div>')
        else:
            self.set_secure_cookie('user', login)
            self.redirect('/')


class Register(BaseHandler):
    def prepare(self):
        return None

    @tornado.gen.coroutine
    def get(self):
        if self.get_current_user() is not None:
            self.redirect('/')
        else:
            self.render('register.html')

    @tornado.gen.coroutine
    def post(self):
        login = xhtml_escape(self.get_argument('login'))
        password = xhtml_escape(self.get_argument('password'))
        name = xhtml_escape(self.get_argument('name'))

        if not login or not password or not name:
            self.render('register.html')
            return

        error = ''
        if not re.match('^[a-zA-Z0-9_]*$', login):
            error = ' You can use only A-Z, a-z, 0-9 and "_" characters for your login.'
        if len(login) > 38:
            error += ' Your login is to long.'
        if len(name) > 58:
            error += ' Your name is to long.'
        if len(password) > 58:
            error += ' Your password is to long.'

        if error:
            self.render('register.html', message=error)
            return

        try:
            cursor_user = yield self.db.execute(create_user(login, name, password, False))
            user = cursor_user.fetchone()
        except IntegrityError:
            self.render('register.html',
                        message='User with this login already exists.' \
                                '<br>Please sign in or choose another login.')
            return

        self.set_secure_cookie('user', login)
        self.redirect('/')


class Logout(BaseHandler):
    def prepare(self):
        return None

    @tornado.gen.coroutine
    def get(self):
        self.clear_cookie('user')
        self.redirect('/login')
