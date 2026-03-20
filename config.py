import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'teacher_platform'
    MYSQL_UNIX_SOCKET = os.environ.get('MYSQL_UNIX_SOCKET') or '/tmp/mysql.sock'
    MYSQL_SSL_CA = os.environ.get('MYSQL_SSL_CA')
    MYSQL_SSL_CA_CONTENT = os.environ.get('MYSQL_SSL_CA_CONTENT')
    MYSQL_CURSORCLASS = 'DictCursor'

    # Microsoft Graph API
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    TENANT_ID = os.environ.get('TENANT_ID') or 'common'
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    REDIRECT_PATH = "/graph-callback"
    SCOPE = ["User.Read", "Mail.Send"]
