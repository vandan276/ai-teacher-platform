from flask import Blueprint, redirect, url_for, request, session, flash
from utils.ms_graph import MicrosoftGraph
from app import mysql

graph_auth_bp = Blueprint('graph_auth', __name__)
graph = MicrosoftGraph()

@graph_auth_bp.route('/login/microsoft')
def login():
    auth_url = graph.get_auth_url()
    return redirect(auth_url)

@graph_auth_bp.route('/graph-callback')
def callback():
    code = request.args.get('code')
    if not code:
        flash('Authentication failed: No code provided.', 'danger')
        return redirect(url_for('auth.login'))
    
    result = graph.acquire_token_by_code(code)
    if 'error' in result:
        flash(f"Authentication failed: {result.get('error_description')}", 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user info from Graph
    user_info = graph.call_graph('/me')
    if not user_info:
        flash('Failed to fetch user info from Microsoft Graph.', 'danger')
        return redirect(url_for('auth.login'))
    
    # User's Microsoft email
    email = user_info.get('mail') or user_info.get('userPrincipalName')
    name = user_info.get('displayName')
    
    # Check if user exists in our DB
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
    
    flash(f"Logged in successfully via Microsoft as {name}!", 'success')
    
    # Redirect based on role
    if user['role'] == 'Admin':
        return redirect(url_for('admin.dashboard'))
    elif user['role'] == 'Employee':
        return redirect(url_for('employee.dashboard'))
    else:
        return redirect(url_for('participant.dashboard'))

@graph_auth_bp.route('/logout/microsoft')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
