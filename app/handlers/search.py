import tornado.gen
from psycopg2.extras import RealDictCursor

from app.handlers import BaseHandler
from app.sql_methods.connections import (
    get_received_invitations,
    get_sent_invitations,
    get_confirmed_connections,
)
from app.sql_methods.users import get_users


class Search(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        if self._data["dataType"] == "html":

            current_user = self.get_current_user()

            cursor_users = yield self.db.execute(
                get_users(), cursor_factory=RealDictCursor
            )

            inv_in_cursor = yield self.db.execute(
                get_received_invitations(login=current_user),
                cursor_factory=RealDictCursor,
            )

            inv_out_cursor = yield self.db.execute(
                get_sent_invitations(login=current_user), cursor_factory=RealDictCursor
            )

            conn_cursor = yield self.db.execute(
                get_confirmed_connections(login=current_user),
                cursor_factory=RealDictCursor,
            )

            users = [
                item.update({"type": "none"}) or item
                for item in cursor_users.fetchall()
            ]
            connections = [
                item.update({"type": "accepted"}) or item
                for item in conn_cursor.fetchall()
            ]
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

            for user in users:
                login = user["login"]
                for con in connections:
                    if login in con.values():
                        user["type"] = con["type"]
                        continue

            self.render(
                "search.html",
                users=users,
                current_user=current_user,
                current_page="search",
            )
