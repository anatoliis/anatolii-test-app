import tornado.gen
from psycopg2.extras import RealDictCursor
from tornado.web import HTTPError

from app.handlers import BaseHandler
from app.sql_methods.connections import (
    get_received_invitations,
    get_sent_invitations,
    get_confirmed_connections,
)
from app.sql_methods.users import get_user_info, get_users_nodes, check_admin


class Index(BaseHandler):
    @tornado.gen.coroutine
    def get(self, login=None):
        current_user = self.get_current_user()

        cursor_admin = yield self.db.execute(check_admin(current_user))
        is_admin = cursor_admin.fetchone()[0]

        if login == current_user:
            self.redirect("/")
            return

        own_page = False
        if login is None:
            login = current_user
            own_page = True

        user_cursor = yield self.db.execute(
            get_user_info(login=login), cursor_factory=RealDictCursor
        )
        user = user_cursor.fetchall()
        if not user:
            raise HTTPError(404)
        user = user[0]

        if own_page:
            status = "own_page"
        else:
            status_cursor = yield self.db.execute(get_users_nodes(current_user, login))
            status_data = status_cursor.fetchall()
            if len(status_data) == 0:
                status = "none"
            elif len(status_data) > 1:
                status = "connected"
            elif status_data[0][0] == current_user:
                status = "sent"
            else:
                status = "received"

        accepted_count = 0
        connections = []

        if is_admin or own_page:
            inv_in_cursor = yield self.db.execute(
                get_received_invitations(login=login), cursor_factory=RealDictCursor
            )
            inv_out_cursor = yield self.db.execute(
                get_sent_invitations(login=login), cursor_factory=RealDictCursor
            )
            accepted_cursor = yield self.db.execute(
                get_confirmed_connections(login=login), cursor_factory=RealDictCursor
            )

            connections = [
                item.update({"type": "accepted"}) or item
                for item in accepted_cursor.fetchall()
            ]

            accepted_count = len(connections)
            connections.extend(
                [
                    item.update({"type": "in"}) or item
                    for item in inv_in_cursor.fetchall()
                ]
            )
            connections.extend(
                [
                    item.update({"type": "out"}) or item
                    for item in inv_out_cursor.fetchall()
                ]
            )

        self.render(
            "index.html",
            is_admin=is_admin,
            status=status,
            page_owner=login,
            current_user=current_user,
            user=user,
            entries=connections,
            conn_count=accepted_count,
            current_page="profile",
        )
