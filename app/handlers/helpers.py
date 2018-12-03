import tornado.gen

from app.handlers import BaseHandler
from app.sql_methods.connections import create_connection
from app.sql_methods.users import create_user


class CreateUsers(BaseHandler):
    def prepare(self):
        return None

    def create_tables(self):
        query = (
            "CREATE TABLE users ( "
            "user_id SERIAL PRIMARY KEY, "
            "login VARCHAR(40) UNIQUE, "
            "name VARCHAR(60), "
            "passw VARCHAR(60), "
            "admin BOOL DEFAULT FALSE); "
            "CREATE TABLE connections ( "
            "user_id INT, "
            "connected INT, "
            "FOREIGN KEY (user_id) REFERENCES users (user_id), "
            "FOREIGN KEY (connected) REFERENCES users (user_id)); "
            "CREATE INDEX index1 "
            "ON connections (user_id, connected); "
            "CREATE INDEX index2 "
            "ON connections (connected, user_id); "
            "INSERT INTO users (login, name, passw, admin) "
            "VALUES ('admin', 'John Smith', 'secret', TRUE );"
        )
        self.db.execute(query)

    @tornado.gen.coroutine
    def get(self):

        self.create_tables()

        # Creating bunch of users
        for i in range(2, 51):
            login = "user_%s" % i
            name = "Name_%s" % i
            passw = "pass%s" % i
            cursor = yield self.db.execute(create_user(login, name, passw, False))
        # End

        # Creating connections
        from random import randrange

        for user in range(1, 51):
            created_connections = []
            for _ in range(randrange(0, 30)):
                connection = randrange(1, 51)
                if connection == user:
                    continue
                if connection in created_connections:
                    continue
                created_connections.append(connection)
                self.db.execute(create_connection(user, connection))
        # End

        self.render("")
