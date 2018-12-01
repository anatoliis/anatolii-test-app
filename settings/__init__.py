DB_PSQL = {'host': 'localhost', 'port': '5433', 'database': 'tl',
           'user': 'tl', 'password': 'tl'}

DB_PSQL_DSN = 'dbname={dbname} user={user} password={password} host={host} port={port}'.format(
    dbname=DB_PSQL['database'], user=DB_PSQL['user'], password=DB_PSQL['password'],
    host=DB_PSQL['host'], port=DB_PSQL['port'])