import tornado.gen
from psycopg2.extras import RealDictCursor

from app.handlers import BaseHandler
from app.sql_methods.users import get_users, get_admins, check_admin


class Admin(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        current_user = self.get_current_user()

        cursor_admin = yield self.db.execute(check_admin(current_user))
        is_admin = cursor_admin.fetchone()[0]

        if not is_admin:
            self.redirect("/")
            return

        cursor_users = yield self.db.execute(get_users(), cursor_factory=RealDictCursor)
        users = cursor_users.fetchall()

        cursor_admins = yield self.db.execute(
            get_admins(), cursor_factory=RealDictCursor
        )
        admins = cursor_admins.fetchall()

        self.render(
            "admin.html",
            users=users,
            admins=admins,
            current_user=current_user,
            current_page="admin",
        )
