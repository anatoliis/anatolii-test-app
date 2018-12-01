from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, xhtml_escape
from jinja2.exceptions import TemplateNotFound


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):

        super().__init__(application, request, **kwargs)
        self._data = {
            'dataType': self.get_argument('data_type', 'html'),
            'body': '',
        }

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        return xhtml_escape(user) if user else None

    @property
    def db(self):
        return self.application.db

    @property
    def env(self):
        return self.application.env

    def prepare(self):
        if self.get_current_user() is None:
            self.redirect(self.get_login_url())
            return

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.redirect('/')
        else:
            self.redirect('/')

    def render(self, template_name, **kwargs):
        if self._data['dataType'] == 'html':
            try:
                template = self.env.get_template(template_name)
            except TemplateNotFound:
                raise HTTPError(404)

            kwargs.update({
                'static_url': self.static_url,
                '_data': self._data,
            })
            render_data = template.render(kwargs)
        else:
            self.add_header('Content-type', 'application/json')
            render_data = json_encode(self._data)

        self.write(render_data)
