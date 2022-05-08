import os

DB_CONN_STRING = "host={} port={} dbname={} user={} password={}".format(
    os.environ.get('DB_HOST', 'localhost'),
    os.environ.get('DB_PORT', 5432),
    os.environ.get('DB_NAME', 'dbname'),
    os.environ.get('DB_USER', 'dbuser'),
    os.environ.get('DB_PASSWORD', '')
)
