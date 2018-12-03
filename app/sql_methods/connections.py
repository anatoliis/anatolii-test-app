def create_connection(user_id, connect_to):
    query = (
        "INSERT INTO connections (user_id, connected) "
        "SELECT {id1}, {id2} "
        "WHERE NOT EXISTS("
        "SELECT 1 FROM connections "
        "WHERE user_id={id1} AND connected={id2});"
    )
    return query.format(id1=user_id, id2=connect_to)


def drop_connection(login, to_drop):
    query = (
        "DELETE "
        "FROM connections c "
        "USING users u, users u2 "
        "WHERE c.user_id=u.user_id "
        "AND c.connected=u2.user_id "
        "AND ( "
        "(u.login='{login}' AND u2.login='{to_drop}') "
        "OR "
        "(u.login='{to_drop}' AND u2.login='{login}'));"
    )
    return query.format(login=login, to_drop=to_drop)


def get_confirmed_connections(login):
    query = (
        "SELECT u2.login, u2.name "
        "FROM users u "
        "RIGHT JOIN connections c1 "
        "ON u.user_id=c1.user_id "
        "INNER JOIN connections c2 "
        "ON c1.user_id=c2.connected AND c1.connected=c2.user_id "
        "LEFT JOIN users u2 "
        "ON c1.connected=u2.user_id "
        "WHERE u.login='{login}' "
        "ORDER BY u2.login ASC;"
    )
    return query.format(login=login)


def get_sent_invitations(login):
    query = (
        "SELECT u2.login, u2.name "
        "FROM users u "
        "RIGHT JOIN connections c1 "
        "ON u.user_id=c1.user_id "
        "LEFT JOIN connections c2 "
        "ON c1.user_id=c2.connected AND c1.connected=c2.user_id "
        "LEFT JOIN users u2 "
        "ON c1.connected=u2.user_id "
        "WHERE c2.user_id IS NULL "
        "AND u.login='{login}' "
        "ORDER BY u2.login ASC;"
    )
    return query.format(login=login)


def get_received_invitations(login):
    query = (
        "SELECT u1.login, u1.name "
        "FROM connections c1 "
        "LEFT JOIN connections c2 "
        "ON c1.user_id=c2.connected AND c2.user_id=c1.connected "
        "LEFT JOIN users u1 "
        "ON c1.user_id=u1.user_id "
        "LEFT JOIN users u2 "
        "ON c1.connected=u2.user_id "
        "WHERE c2.connected IS NULL "
        "AND u2.login='{login}';"
    )
    return query.format(login=login)
