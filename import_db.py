import mysql.connector
import os
import tempfile
from dotenv import load_dotenv

# Load local .env for local testing if needed
load_dotenv()

import sys

def import_db():
    print("Starting Database Migration...", file=sys.stderr, flush=True)
    
    # Get config from Environment Variables (Prioritize Railway's Public Names)
    env_mysql_host = os.environ.get('MYSQLHOST')
    host = env_mysql_host or os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD')
    database = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB')
    port = os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT') or 3306
    ssl_ca_content = os.environ.get('MYSQL_SSL_CA_CONTENT')

    # Force ignore internal host if it was accidentally kept
    if host and '.internal' in host:
        print(f"DEBUG: Ignoring internal host {host}, looking for public one...", file=sys.stderr, flush=True)
        if env_mysql_host and '.internal' not in env_mysql_host:
             host = env_mysql_host

    if not all([host, user, password, database]):
        print(f"ERROR: Missing database environment variables! (Host: {host}, User: {user}, DB: {database})", file=sys.stderr, flush=True)
        return

    ca_path = None
    # Use a temporary file for the SSL CA if provided
    if ssl_ca_content:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pem') as tf:
            tf.write(ssl_ca_content.encode())
            ca_path = tf.name

    try:
        print(f"DEBUG: Attempting to connect to {host}:{port} (SSL: {bool(ca_path)})...", file=sys.stderr, flush=True)
        conn_args = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': int(port),
            'connect_timeout': 15
        }
        if ca_path:
            conn_args['ssl_ca'] = ca_path
            
        conn = mysql.connector.connect(**conn_args)
        print("DEBUG: Connection established!", file=sys.stderr, flush=True)
        cursor = conn.cursor()
        
        print(f"DEBUG: Reading backup.sql...", file=sys.stderr, flush=True)
        with open('backup.sql', 'r') as f:
            lines = f.readlines()
        
        # Filter out lines that require SUPER privileges (GTID, LOG_BIN, etc.)
        filtered_lines = []
        for line in lines:
            if any(term in line.upper() for term in ['GTID_PURGED', 'SQL_LOG_BIN', 'GLOBAL.']):
                print(f"Skipping restricted line: {line.strip()[:50]}...", file=sys.stderr, flush=True)
                continue
            filtered_lines.append(line)
        
        sql_content = "".join(filtered_lines)
        
        # Use multi=True for efficient execution
        print(f"Starting SQL execution ({len(filtered_lines)} lines)...", file=sys.stderr, flush=True)
        results = cursor.execute(sql_content, multi=True)
        count = 0
        for result in results:
            count += 1
            if count % 20 == 0:
                print(f"Executed {count} batches...", file=sys.stderr, flush=True)
        
        conn.commit()
        print(f"SUCCESS: Database migration completed! {count} iterations.", file=sys.stderr, flush=True)
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}", file=sys.stderr, flush=True)
        raise e # Re-raise so app.py can catch it and show to user
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
        # Cleanup temp CA file
        if ca_path and os.path.exists(ca_path):
            os.remove(ca_path)

if __name__ == "__main__":
    import_db()
