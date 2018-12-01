import tornado.gen

from tornado.escape import json_decode, json_encode

from app.handlers import BaseHandler
from app.sql_methods.connections import drop_connection, create_connection
from app.sql_methods.users import get_users_ids, check_admin, drop_user


class Ajax(BaseHandler):
    @tornado.gen.coroutine
    def put(self):
        current_user = self.get_current_user()

        data = json_decode(self.request.body)

        if data['action'] == 'conn_remove':
            target_user = data['target']
            self.db.execute(drop_connection(current_user, target_user))
            self._data['body'] = json_encode({'status': 'ok'})

        elif data['action'] == 'conn_create':
            target_user = data['target']
            ids_cursor = yield self.db.execute(get_users_ids(current_user, target_user))
            ids = [id[0] for id in ids_cursor.fetchall()]
            self.db.execute(create_connection(ids[0], ids[1]))
            self._data['body'] = json_encode({'status': 'ok'})

        elif data['action'] == 'user_remove':
            current_user = self.get_current_user()
            cursor_admin = yield self.db.execute(check_admin(current_user))
            is_admin = cursor_admin.fetchone()[0]
            if is_admin:
                target_user = data['target']
                self.db.execute(drop_user(target_user))
                self._data['body'] = json_encode({'status': 'ok'})
            else:
                self._data['body'] = json_encode({'status': 'access_error'})

        self.render('')