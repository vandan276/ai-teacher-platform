import mysql.connector
import os
import tempfile
from dotenv import load_dotenv

# Load local .env for local testing if needed
load_dotenv()

import sys

def import_db():
    print("Starting Database Migration...", file=sys.stderr, flush=True)
    
    # Get config from Environment Variables (set these on Render!)
    host = os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
    database = os.environ.get('MYSQL_DB')
    port = os.environ.get('MYSQL_PORT', 25060)
    ssl_ca_content = os.environ.get('MYSQL_SSL_CA_CONTENT')

    if not all([host, user, password, database, ssl_ca_content]):
        print(f"ERROR: Missing database environment variables! (Host: {bool(host)}, User: {bool(user)}, Pass: {bool(password)}, DB: {bool(database)}, SSL: {bool(ssl_ca_content)})", file=sys.stderr, flush=True)
        return

    # Use a temporary file for the SSL CA
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pem') as tf:
        tf.write(ssl_ca_content.encode())
        ca_path = tf.name

    try:
        print(f"DEBUG: Attempting to connect to {host}:{port}...", file=sys.stderr, flush=True)
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl_ca=ca_path,
            connect_timeout=10 # Add timeout to prevent hanging forever
        )
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
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
        # Cleanup temp CA file
        if os.path.exists(ca_path):
            os.remove(ca_path)

if __name__ == "__main__":
    import_db()
