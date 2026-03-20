import mysql.connector
from flask import current_app, g

class ConnectionWrapper:
    def __init__(self, connection):
        self._connection = connection

    def cursor(self, *args, **kwargs):
        # Always return dictionary cursor to match DictCursor behavior
        kwargs['dictionary'] = True
        return self._connection.cursor(*args, **kwargs)

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        return self._connection.close()

class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MYSQL_HOST', 'localhost')
        app.config.setdefault('MYSQL_USER', 'root')
        app.config.setdefault('MYSQL_PASSWORD', '')
        app.config.setdefault('MYSQL_DB', None)
        app.config.setdefault('MYSQL_PORT', 3306)
        app.config.setdefault('MYSQL_UNIX_SOCKET', None)

    @property
    def connection(self):
        if 'mysql_db' not in g:
            import sys
            try:
                port = current_app.config.get('MYSQL_PORT', 3306)
                if isinstance(port, str) and port.isdigit():
                    port = int(port)
                
                config = {
                    'host': current_app.config['MYSQL_HOST'],
                    'user': current_app.config['MYSQL_USER'],
                    'password': current_app.config['MYSQL_PASSWORD'],
                    'database': current_app.config['MYSQL_DB'],
                    'port': port,
                    'connect_timeout': 10
                }
                
                ssl_ca_content = current_app.config.get('MYSQL_SSL_CA_CONTENT')
                if ssl_ca_content and len(ssl_ca_content.strip()) > 10:
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pem') as tf:
                        tf.write(ssl_ca_content.encode())
                        config['ssl_ca'] = tf.name
                elif current_app.config.get('MYSQL_SSL_CA'):
                    config['ssl_ca'] = current_app.config['MYSQL_SSL_CA']
                
                conn = mysql.connector.connect(**config)
                g.mysql_db = ConnectionWrapper(conn)
            except Exception as e:
                print(f"CRITICAL: MySQL Connection Failed: {e}", file=sys.stderr, flush=True)
                return None
        return g.mysql_db
