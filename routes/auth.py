from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user['password_hash'], password):
                
                session['user_id'] = user['id']
                session['name'] = user['name']
                session['role'] = user['role']
                session['district_id'] = user['district_id']
                
                if user['role'] == 'Admin':
                    return redirect(url_for('admin.dashboard'))
                elif user['role'] == 'Employee':
                    return redirect(url_for('employee.dashboard'))
                else:
                    return redirect(url_for('participant.welcome'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            print(f"DEBUG: Login connection failed: {e}")
            flash('Database connection error. Please ensure your MySQL server is running.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    districts = []
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM districts")
        districts = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"DEBUG: Register load districts failed: {e}", flush=True)
        flash('Database connection error. districts could not be loaded.', 'danger')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        district_id = request.form.get('district_id')

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, password_hash, role, district_id, is_approved) VALUES (%s, %s, %s, 'Participant', %s, TRUE)",
                        (name, email, hashed_password, district_id))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"DEBUG: Register save failed: {e}")
            flash('Email already exists or database error occurred.', 'danger')

    return render_template('register.html', districts=districts)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
