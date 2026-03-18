from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import mysql
from utils.decorators import role_required, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('Admin')
def dashboard():
    cur = mysql.connection.cursor()
    
    # Stats
    cur.execute("SELECT COUNT(*) as count FROM users WHERE role = 'Participant'")
    total_teachers = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM districts")
    total_districts = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM modules")
    total_modules = cur.fetchone()['count']
    
    # District-wise progress (simplified for now)
    cur.execute("""
        SELECT d.district_name, COUNT(u.id) as teacher_count 
        FROM districts d 
        LEFT JOIN users u ON d.id = u.district_id AND u.role = 'Participant'
        GROUP BY d.id
    """)
    district_stats = cur.fetchall()
    
    # Platform Engagement (Last 7 Days)
    cur.execute("""
        SELECT DATE(timestamp) as date, COUNT(*) as count 
        FROM results 
        WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
        GROUP BY DATE(timestamp) 
        ORDER BY date ASC
    """)
    engagement_data_raw = cur.fetchall()
    
    # Fill in missing dates for the last 7 days
    engagement_map = {row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], (datetime, timedelta)) or hasattr(row['date'], 'strftime') else str(row['date']): row['count'] for row in engagement_data_raw}
    engagement_labels = []
    engagement_values = []
    
    for i in range(6, -1, -1):
        d = (datetime.now() - timedelta(days=i)).date()
        date_str = d.strftime('%Y-%m-%d')
        engagement_labels.append(d.strftime('%b %d'))
        engagement_values.append(engagement_map.get(date_str, 0))

    cur.close()
    return render_template('admin/dashboard.html', 
                           total_teachers=total_teachers, 
                           total_districts=total_districts, 
                           total_modules=total_modules,
                           district_stats=district_stats,
                           engagement_labels=engagement_labels,
                           engagement_values=engagement_values)

@admin_bp.route('/users')
@login_required
@role_required('Admin')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT u.*, d.district_name FROM users u LEFT JOIN districts d ON u.district_id = d.id ORDER BY u.role, u.name")
    all_users = cur.fetchall()
    
    # Get districts for the "Add Employee" modal
    cur.execute("SELECT * FROM districts")
    districts = cur.fetchall()
    
    cur.close()
    return render_template('admin/users.html', users=all_users, districts=districts)

@admin_bp.route('/users/add', methods=['POST'])
@login_required
@role_required('Admin')
def add_employee():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    district_id = request.form.get('district_id')
    
    if not name or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('admin.users'))
        
    hashed_password = generate_password_hash(password)
    
    try:
        cur = mysql.connection.cursor()
        # Inserting as Employee with is_approved=True
        cur.execute("""
            INSERT INTO users (name, email, password_hash, role, district_id, is_approved) 
            VALUES (%s, %s, %s, 'Employee', %s, TRUE)
        """, (name, email, hashed_password, district_id if district_id else None))
        mysql.connection.commit()
        cur.close()
        flash(f'Employee {name} added successfully.', 'success')
    except Exception as e:
        flash('Error adding employee. Email may already exist.', 'danger')
        print(f"DEBUG: Add employee failed: {e}")
        
    return redirect(url_for('admin.users'))

@admin_bp.route('/approve/<int:user_id>')
@login_required
@role_required('Admin')
def approve_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_approved = TRUE WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    flash('User approved successfully.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/modules', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def modules():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        cur.execute("INSERT INTO modules (title, description, content) VALUES (%s, %s, %s)", (title, description, content))
        mysql.connection.commit()
        flash('Module created successfully.', 'success')
        return redirect(url_for('admin.modules'))
    
    cur.execute("SELECT * FROM modules")
    all_modules = cur.fetchall()
    cur.close()
    return render_template('admin/modules.html', modules=all_modules)

@admin_bp.route('/modules/delete/<int:module_id>')
@login_required
@role_required('Admin')
def delete_module(module_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM modules WHERE id = %s", (module_id,))
    mysql.connection.commit()
    cur.close()
    flash('Module deleted successfully.', 'info')
    return redirect(url_for('admin.modules'))

@admin_bp.route('/modules/<int:module_id>/assessments', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def manage_assessments(module_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        question = request.form.get('question')
        a = request.form.get('option_a')
        b = request.form.get('option_b')
        c = request.form.get('option_c')
        d = request.form.get('option_d')
        correct = request.form.get('correct_answer')
        cur.execute("""
            INSERT INTO assessments (module_id, question, option_a, option_b, option_c, option_d, correct_answer) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (module_id, question, a, b, c, d, correct))
        mysql.connection.commit()
        flash('Assessment question added.', 'success')
    
    cur.execute("SELECT * FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()
    cur.execute("SELECT * FROM assessments WHERE module_id = %s", (module_id,))
    questions = cur.fetchall()
    cur.close()
    return render_template('admin/manage_assessments.html', module=module, questions=questions)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_user(user_id):
    cur = mysql.connection.cursor()
    # Ensure we don't delete ourselves (though role check handles it, safety first)
    if user_id == session.get('user_id'):
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
        
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        flash('User deleted successfully.', 'info')
    except Exception as e:
        flash('Error deleting user.', 'danger')
        print(f"DEBUG: Delete user failed: {e}")
    finally:
        cur.close()
        
    return redirect(url_for('admin.users'))

@admin_bp.route('/resources', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def resources():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        file_url = request.form.get('file_url')
        
        if not title or not file_url:
            flash('Title and File URL are required.', 'danger')
        else:
            cur.execute("INSERT INTO resources (title, description, category, file_url) VALUES (%s, %s, %s, %s)",
                        (title, description, category, file_url))
            mysql.connection.commit()
            flash('Resource added successfully.', 'success')
        return redirect(url_for('admin.resources'))
    
    cur.execute("SELECT * FROM resources ORDER BY id DESC")
    all_resources = cur.fetchall()
    cur.close()
    return render_template('admin/resources.html', resources=all_resources)

@admin_bp.route('/resources/delete/<int:resource_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_resource(resource_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM resources WHERE id = %s", (resource_id,))
    mysql.connection.commit()
    cur.close()
    flash('Resource deleted.', 'info')
    return redirect(url_for('admin.resources'))

@admin_bp.route('/messages')
@login_required
@role_required('Admin')
def messages():
    employee_id = request.args.get('employee_id', type=int)
    cur = mysql.connection.cursor()
    
    # Get all employees
    cur.execute("SELECT id, name, email FROM users WHERE role = 'Employee' AND is_approved = TRUE")
    employees = cur.fetchall()
    
    selected_employee = None
    chat_history = []
    
    if employee_id:
        cur.execute("SELECT id, name FROM users WHERE id = %s AND role = 'Employee'", (employee_id,))
        selected_employee = cur.fetchone()
        
        if selected_employee:
            # Get chat history
            cur.execute("""
                SELECT m.*, s.name as sender_name 
                FROM messages m 
                JOIN users s ON m.sender_id = s.id 
                WHERE (m.sender_id = %s AND m.receiver_id = %s) 
                   OR (m.sender_id = %s AND m.receiver_id = %s)
                ORDER BY m.timestamp ASC
            """, (session['user_id'], employee_id, employee_id, session['user_id']))
            chat_history = cur.fetchall()
            
            # Mark messages as read
            cur.execute("UPDATE messages SET is_read = TRUE WHERE receiver_id = %s AND sender_id = %s", (session['user_id'], employee_id))
            mysql.connection.commit()
            
    cur.close()
    return render_template('admin/messages.html', 
                           employees=employees, 
                           selected_employee=selected_employee, 
                           chat_history=chat_history)

@admin_bp.route('/messages/send', methods=['POST'])
@login_required
@role_required('Admin')
def send_message():
    receiver_id = request.form.get('receiver_id', type=int)
    message_text = request.form.get('message')
    
    if not receiver_id or not message_text:
        flash('Recipient and message text are required.', 'danger')
        return redirect(url_for('admin.messages'))
        
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
                (session['user_id'], receiver_id, message_text))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('admin.messages', employee_id=receiver_id))

@admin_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def announcements():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority', 'normal')
        
        if title and message:
            cur.execute("INSERT INTO announcements (title, message, priority, created_by) VALUES (%s, %s, %s, %s)",
                        (title, message, priority, session['user_id']))
            mysql.connection.commit()
            flash('Announcement published successfully!', 'success')
        else:
            flash('Title and message are required.', 'danger')
        return redirect(url_for('admin.announcements'))
    
    cur.execute("SELECT a.*, u.name as author_name FROM announcements a JOIN users u ON a.created_by = u.id ORDER BY a.created_at DESC")
    all_announcements = cur.fetchall()
    cur.close()
    return render_template('admin/announcements.html', announcements=all_announcements)

@admin_bp.route('/announcements/delete/<int:announcement_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_announcement(announcement_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM announcements WHERE id = %s", (announcement_id,))
    mysql.connection.commit()
    cur.close()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/events', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def events():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_type = request.form.get('event_type', 'event')
        event_date = request.form.get('event_date')
        event_time = request.form.get('event_time')
        location = request.form.get('location')
        
        if title and event_date:
            cur.execute("""INSERT INTO events (title, description, event_type, event_date, event_time, location, created_by) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (title, description, event_type, event_date, event_time or None, location, session['user_id']))
            mysql.connection.commit()
            flash('Event created successfully!', 'success')
        else:
            flash('Title and date are required.', 'danger')
        return redirect(url_for('admin.events'))
    
    cur.execute("SELECT * FROM events ORDER BY event_date ASC")
    all_events = cur.fetchall()
    cur.close()
    return render_template('admin/events.html', events=all_events)

@admin_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
@role_required('Admin')
def delete_event(event_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mysql.connection.commit()
    cur.close()
    flash('Event deleted.', 'info')
    return redirect(url_for('admin.events'))
