import os
import requests
from flask import Blueprint, redirect, url_for, request, session, flash
from app import mysql

google_auth_bp = Blueprint('google_auth', __name__)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

# Using the standard Google OAuth 2.0 endpoints
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

@google_auth_bp.route('/login/google')
def login():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        flash('Google Login is not configured. Please add keys to .env', 'warning')
        return redirect(url_for('auth.login'))
        
    redirect_uri = url_for('google_auth.callback', _external=True)
    
    # Generate the OAuth authorization URL
    auth_url = (
        f"{AUTHORIZATION_BASE_URL}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=online"
    )
    return redirect(auth_url)

@google_auth_bp.route('/google-callback')
def callback():
    code = request.args.get('code')
    if not code:
        flash('Authentication failed or cancelled by user.', 'danger')
        return redirect(url_for('auth.login'))
        
    redirect_uri = url_for('google_auth.callback', _external=True)
    
    # Exchange auth code for access token
    token_response = requests.post(TOKEN_URL, data={
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    })
    
    if token_response.status_code != 200:
        flash('Failed to retrieve access token from Google.', 'danger')
        return redirect(url_for('auth.login'))
        
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    
    # Use access token to fetch user info
    user_info_response = requests.get(USER_INFO_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })
    
    if user_info_response.status_code != 200:
        flash('Failed to fetch user info from Google.', 'danger')
        return redirect(url_for('auth.login'))
        
    user_info = user_info_response.json()
    email = user_info.get('email')
    name = user_info.get('name')
    
    if not email:
        flash('Google account did not return an email address.', 'danger')
        return redirect(url_for('auth.login'))
        
    # Check if user exists in DB
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    
    if not user:
        # Auto-register as 'Participant' and auto-approve for SSO users
        cur.execute("""
            INSERT INTO users (name, email, password_hash, role, is_approved) 
            VALUES (%s, %s, 'OAUTH_USER', 'Participant', TRUE)
        """, (name, email))
        mysql.connection.commit()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
    cur.close()
    
    # Store user in session
    session['user_id'] = user['id']
    session['name'] = user['name']
    session['email'] = user['email']
    session['role'] = user['role']
    
    flash(f"Logged in successfully via Google as {name}!", 'success')
    
    # Redirect based on role
    if user['role'] == 'Admin':
        return redirect(url_for('admin.dashboard'))
    elif user['role'] == 'Employee':
        return redirect(url_for('employee.dashboard'))
    else:
        return redirect(url_for('participant.dashboard'))
