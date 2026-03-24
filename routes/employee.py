from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import mysql
from utils.decorators import role_required, login_required

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/dashboard')
@login_required
@role_required('Employee')
def dashboard():
    cur = mysql.connection.cursor()
    
    # Get all districts for the dropdown
    cur.execute("SELECT * FROM districts")
    districts = cur.fetchall()
    
    selected_district = request.args.get('district_id')
    
    teachers = []
    if selected_district:
        cur.execute("""
            SELECT u.*, 
                   (SELECT COUNT(*) FROM progress p WHERE p.user_id = u.id AND p.completed = TRUE) as completed_modules,
                   (SELECT COUNT(*) FROM trophies t WHERE t.user_id = u.id AND t.achieved = TRUE) as trophy
            FROM users u 
            WHERE u.district_id = %s AND u.role = 'Participant'
        """, (selected_district,))
        teachers = cur.fetchall()
        
    # Get upcoming events for widget
    cur.execute("SELECT * FROM events WHERE event_date >= CURDATE() ORDER BY event_date ASC LIMIT 3")
    upcoming_events = cur.fetchall()
    
    cur.close()
    return render_template('employee/dashboard.html', 
                           districts=districts, 
                           teachers=teachers, 
                           selected_district=selected_district,
                           upcoming_events=upcoming_events)

@employee_bp.route('/all-users')
@login_required
@role_required('Employee')
def all_users():
    cur = mysql.connection.cursor()
    # Search and filter support
    search_query = request.args.get('q', '')
    role_filter = request.args.get('role', '')

    sql = """
        SELECT u.id, u.name, u.email, u.role, u.is_approved, d.district_name
        FROM users u
        LEFT JOIN districts d ON u.district_id = d.id
        WHERE 1=1
    """
    params = []
    if search_query:
        sql += " AND (u.name LIKE %s OR u.email LIKE %s)"
        params.extend([f'%{search_query}%', f'%{search_query}%'])
    if role_filter:
        sql += " AND u.role = %s"
        params.append(role_filter)
    sql += " ORDER BY u.role, u.name"
    
    cur.execute(sql, params)
    all_users_list = cur.fetchall()
    cur.close()
    return render_template('employee/all_users.html', users=all_users_list, search_query=search_query, role_filter=role_filter)

@employee_bp.route('/messages')
@login_required
@role_required('Employee')
def messages():
    cur = mysql.connection.cursor()
    
    # Get all Admins and other Employees as contacts
    cur.execute("""
        SELECT id, name, email, role FROM users 
        WHERE (role = 'Admin' OR role = 'Employee') AND id != %s AND is_approved = TRUE
        ORDER BY role, name
    """, (session['user_id'],))
    contacts = cur.fetchall()
    
    contact_id = request.args.get('contact_id', type=int)
    if not contact_id and contacts:
        contact_id = contacts[0]['id']
        
    selected_contact = None
    chat_history = []
    
    if contact_id:
        cur.execute("SELECT id, name, role FROM users WHERE id = %s", (contact_id,))
        selected_contact = cur.fetchone()
        
        if selected_contact:
            cur.execute("""
                SELECT m.*, s.name as sender_name 
                FROM messages m 
                JOIN users s ON m.sender_id = s.id 
                WHERE (m.sender_id = %s AND m.receiver_id = %s) 
                   OR (m.sender_id = %s AND m.receiver_id = %s)
                ORDER BY m.timestamp ASC
            """, (session['user_id'], contact_id, contact_id, session['user_id']))
            chat_history = cur.fetchall()
            
            cur.execute("UPDATE messages SET is_read = TRUE WHERE receiver_id = %s AND sender_id = %s", (session['user_id'], contact_id))
            mysql.connection.commit()
            
    cur.close()
    return render_template('employee/messages.html', 
                           contacts=contacts, 
                           selected_contact=selected_contact, 
                           chat_history=chat_history)

@employee_bp.route('/messages/send', methods=['POST'])
@login_required
@role_required('Employee')
def send_message():
    receiver_id = request.form.get('receiver_id', type=int)
    message_text = request.form.get('message')
    
    if not receiver_id or not message_text:
        return {'error': 'Missing data'}, 400
        
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
                (session['user_id'], receiver_id, message_text))
    mysql.connection.commit()
    cur.close()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return {'status': 'success'}
    return redirect(url_for('employee.messages', contact_id=receiver_id))

@employee_bp.route('/messages/fetch/<int:contact_id>')
@login_required
@role_required('Employee')
def fetch_chat(contact_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, role FROM users WHERE id = %s", (contact_id,))
    selected_contact = cur.fetchone()
    
    cur.execute("""
        SELECT m.*, s.name as sender_name 
        FROM messages m 
        JOIN users s ON m.sender_id = s.id 
        WHERE (m.sender_id = %s AND m.receiver_id = %s) 
           OR (m.sender_id = %s AND m.receiver_id = %s)
        ORDER BY m.timestamp ASC
    """, (session['user_id'], contact_id, contact_id, session['user_id']))
    chat_history = cur.fetchall()
    
    cur.execute("UPDATE messages SET is_read = TRUE WHERE receiver_id = %s AND sender_id = %s", (session['user_id'], contact_id))
    mysql.connection.commit()
    cur.close()
    
    return render_template('shared/_chat_history.html', chat_history=chat_history, selected_contact=selected_contact)

@employee_bp.route('/resources')
@login_required
@role_required('Employee')
def resources():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resources ORDER BY category ASC, title ASC")
    resources_list = cur.fetchall()
    cur.close()
    return render_template('participant/resources.html', resources=resources_list)

@employee_bp.route('/calendar')
@login_required
@role_required('Employee')
def calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE event_date >= CURDATE() ORDER BY event_date ASC, event_time ASC")
    upcoming_events = cur.fetchall()
    cur.execute("SELECT * FROM events WHERE event_date < CURDATE() ORDER BY event_date DESC LIMIT 5")
    past_events = cur.fetchall()
    cur.close()
    return render_template('participant/calendar.html', upcoming_events=upcoming_events, past_events=past_events)
