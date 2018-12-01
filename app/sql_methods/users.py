def create_user(login, name, passw, admin=False):
    admin = 'TRUE' if admin else 'FALSE'
    query = "INSERT INTO users " \
            "(login, name, admin, passw) " \
            "VALUES ('{login}', '{name}', {admin}, '{passw}') " \
            "RETURNING user_id;"
    return query.format(login=login, name=name, admin=admin, passw=passw)


def drop_user(login):
    query = "DELETE FROM connections c " \
            "USING users u, users u2 " \
            "WHERE c.user_id=u.user_id " \
            "AND c.connected=u2.user_id " \
            "AND (u.login='{login}' " \
            "OR u2.login='{login}'); "

    query += "DELETE FROM users " \
             "WHERE login='{login}';"
    return query.format(login=login)


def get_users_ids(user1, user2):
    query = "SELECT user_id " \
            "FROM users " \
            "WHERE login='{user1}' " \
            "OR login='{user2}' " \
            "ORDER BY CASE WHEN login='{user1}' THEN 1 " \
            "WHEN login='{user2}' THEN 2 END ASC;"
    return query.format(user1=user1, user2=user2)


def get_user_info(login):
    query = "SELECT * FROM users " \
            "WHERE login='{login}';"
    return query.format(login=login)


def check_admin(login):
    query = "SELECT admin FROM users " \
            "WHERE login='{login}';"
    return query.format(login=login)


def get_admins():
    query = "SELECT * FROM users " \
            "WHERE admin=TRUE;"
    return query


def get_users():
    query = "SELECT u.login, u.name, u.admin, COUNT(c.user_id) as \"connections\"" \
            "FROM users u " \
            "LEFT JOIN connections c ON u.user_id = c.user_id " \
            "GROUP BY u.user_id " \
            "ORDER BY u.user_id ASC;"
    return query


def get_users_nodes(user1, user2):
    query = "SELECT u.login as username, u2.login as target " \
            "FROM connections c " \
            "LEFT JOIN users u " \
            "ON c.user_id = u.user_id " \
            "LEFT JOIN users u2 " \
            "ON c.connected = u2.user_id " \
            "WHERE u.login = '{user1}' " \
            "AND u2.login = '{user2}' " \
            "OR u.login = '{user2}' " \
            "AND u2.login = '{user1}';"
    return query.format(user1=user1, user2=user2)
