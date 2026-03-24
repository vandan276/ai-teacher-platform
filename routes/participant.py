from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import mysql
from utils.decorators import role_required, login_required

participant_bp = Blueprint('participant', __name__)

@participant_bp.route('/welcome')
@login_required
@role_required('Participant')
def welcome():
    user_name = session.get('name', 'Participant')
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) as count FROM modules")
    total_modules = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM progress WHERE user_id = %s AND completed = TRUE", (session['user_id'],))
    completed = cur.fetchone()['count']
    cur.close()
    return render_template('participant/welcome.html', user_name=user_name, total_modules=total_modules, completed_modules=completed)

@participant_bp.route('/dashboard')
@login_required
@role_required('Participant')
def dashboard():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    # Get user points
    cur.execute("SELECT points FROM users WHERE id = %s", (user_id,))
    points_data = cur.fetchone()
    points = points_data['points'] if points_data else 0
    
    # Get user badges
    cur.execute("""
        SELECT b.* FROM badges b 
        JOIN user_badges ub ON b.id = ub.badge_id 
        WHERE ub.user_id = %s
    """, (user_id,))
    badges = cur.fetchall()
    
    # Get total modules
    cur.execute("SELECT COUNT(*) as count FROM modules")
    total_modules = cur.fetchone()['count']
    
    # Get completed modules
    cur.execute("SELECT COUNT(*) as count FROM progress WHERE user_id = %s AND completed = TRUE", (user_id,))
    completed_modules = cur.fetchone()['count']
    
    # Get module list with progress
    cur.execute("""
        SELECT m.*, p.completed 
        FROM modules m 
        LEFT JOIN progress p ON m.id = p.module_id AND p.user_id = %s
    """, (user_id,))
    modules = cur.fetchall()
    
    has_trophy = (completed_modules == total_modules) if total_modules > 0 else False
    
    # Get upcoming events for widget
    cur.execute("SELECT * FROM events WHERE event_date >= CURDATE() ORDER BY event_date ASC LIMIT 3")
    upcoming_events = cur.fetchall()
    
    cur.close()
    return render_template('participant/dashboard.html', 
                           total_modules=total_modules, 
                           completed_modules=completed_modules, 
                           points=points,
                           badges=badges,
                           modules=modules,
                           has_trophy=has_trophy,
                           upcoming_events=upcoming_events)

@participant_bp.route('/module/<int:module_id>')
@login_required
@role_required('Participant')
def module_detail(module_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()
    cur.close()
    return render_template('participant/module_detail.html', module=module)

@participant_bp.route('/module/<int:module_id>/assessment', methods=['GET', 'POST'])
@login_required
@role_required('Participant')
def assessment(module_id):
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        # Evaluation Logic
        cur.execute("SELECT * FROM assessments WHERE module_id = %s", (module_id,))
        questions = cur.fetchall()
        
        score = 0
        total = len(questions)
        
        for q in questions:
            user_answer = request.form.get(f"q_{q['id']}")
            if user_answer == q['correct_answer']:
                score += 1
        
        percentage = (score / total * 100) if total > 0 else 0
        passed = percentage >= 80 # 80% passing criteria
        
        # Save Result
        cur.execute("INSERT INTO results (user_id, module_id, score, passed) VALUES (%s, %s, %s, %s)",
                    (user_id, module_id, score, passed))
        
        if passed:
            from utils.gamification import award_points, check_and_award_badges
            
            cur.execute("INSERT INTO progress (user_id, module_id, completed) VALUES (%s, %s, TRUE) ON DUPLICATE KEY UPDATE completed = TRUE",
                        (user_id, module_id))
            
            # Award points and badges
            award_points(user_id, 100) # Base points
            if percentage == 100:
                award_points(user_id, 50) # Bonus for perfect score
            
            check_and_award_badges(user_id)
            
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('participant.results', module_id=module_id, score=score, total=total, passed=passed))

    cur.execute("SELECT * FROM assessments WHERE module_id = %s", (module_id,))
    questions = cur.fetchall()
    cur.execute("SELECT * FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()
    cur.close()
    return render_template('participant/assessment.html', module=module, questions=questions)

@participant_bp.route('/results')
@login_required
@role_required('Participant')
def results():
    module_id = request.args.get('module_id')
    score = request.args.get('score')
    total = request.args.get('total')
    passed = request.args.get('passed') == 'True'
    return render_template('participant/results.html', module_id=module_id, score=score, total=total, passed=passed)

@participant_bp.route('/certificate')
@login_required
@role_required('Participant')
def certificate():
    from utils.certificate import generate_certificate_url
    user_id = session['user_id']
    user_name = session['name']
    
    cur = mysql.connection.cursor()
    # Double check completion
    cur.execute("SELECT COUNT(*) as count FROM modules")
    total_m = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM progress WHERE user_id = %s AND completed = TRUE", (user_id,))
    comp_m = cur.fetchone()['count']
    cur.close()
    
    if total_m > 0 and total_m == comp_m:
        cert_url = generate_certificate_url(user_name)
        if cert_url:
            return render_template('participant/certificate_view.html', cert_url=cert_url)
        else:
            flash('Failed to generate certificate. Please contact admin.', 'danger')
    else:
        flash('You must complete all modules to earn a certificate.', 'warning')
        
    return redirect(url_for('participant.dashboard'))

@participant_bp.route('/roadmap')
@login_required
@role_required('Participant')
def roadmap():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.*, p.completed 
        FROM modules m 
        LEFT JOIN progress p ON m.id = p.module_id AND p.user_id = %s
        ORDER BY m.id ASC
    """, (user_id,))
    modules = cur.fetchall()
    cur.close()
    return render_template('participant/roadmap.html', modules=modules)

@participant_bp.route('/analytics')
@login_required
@role_required('Participant')
def analytics():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get completion by category
    cur.execute("""
        SELECT category, 
               COUNT(*) as total,
               SUM(CASE WHEN p.completed THEN 1 ELSE 0 END) as completed,
               AVG(CASE WHEN r.passed THEN r.score ELSE NULL END) as avg_score
        FROM modules m
        LEFT JOIN progress p ON m.id = p.module_id AND p.user_id = %s
        LEFT JOIN results r ON m.id = r.module_id AND r.user_id = %s
        GROUP BY category
    """, (user_id, user_id))
    stats = cur.fetchall()
    cur.close()
    
    return render_template('participant/analytics.html', stats=stats)

@participant_bp.route('/hall-of-fame')
@login_required
def hall_of_fame():
    cur = mysql.connection.cursor()
    
    # Get total modules for status calculation
    cur.execute("SELECT COUNT(*) as cnt FROM modules")
    total_modules = cur.fetchone()['cnt'] or 0
    
    # Get top 10 players based on points
    cur.execute("""
        SELECT u.name, d.district_name, COALESCE(u.points, 0) as points,
               (SELECT COUNT(*) FROM progress p WHERE p.user_id = u.id AND p.completed = TRUE) as completed_count,
               (SELECT ROUND(AVG(r.score * 100.0 / 
                   (SELECT COUNT(*) FROM assessments a WHERE a.module_id = r.module_id)), 1) 
                FROM results r WHERE r.user_id = u.id AND r.passed = TRUE) as avg_score
        FROM users u
        LEFT JOIN districts d ON u.district_id = d.id
        WHERE u.role = 'Participant' AND u.is_approved = TRUE
        ORDER BY points DESC, completed_count DESC
        LIMIT 10
    """)
    leaderboard = cur.fetchall()
    cur.close()
    return render_template('participant/hall_of_fame.html', leaderboard=leaderboard, total_modules=total_modules)

@participant_bp.route('/resources')
@login_required
@role_required('Participant')
def resources():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resources ORDER BY category ASC, title ASC")
    resources = cur.fetchall()
    cur.close()
    return render_template('participant/resources.html', resources=resources)

@participant_bp.route('/calendar')
@login_required
def calendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE event_date >= CURDATE() ORDER BY event_date ASC, event_time ASC")
    upcoming_events = cur.fetchall()
    cur.execute("SELECT * FROM events WHERE event_date < CURDATE() ORDER BY event_date DESC LIMIT 5")
    past_events = cur.fetchall()
    cur.close()
    return render_template('participant/calendar.html', upcoming_events=upcoming_events, past_events=past_events)

@participant_bp.route('/notifications')
@login_required
def notifications():
    cur = mysql.connection.cursor()
    cur.execute("SELECT a.*, u.name as author_name FROM announcements a JOIN users u ON a.created_by = u.id ORDER BY a.created_at DESC")
    all_announcements = cur.fetchall()
    cur.close()
    return render_template('participant/notifications.html', announcements=all_announcements)

@participant_bp.route('/showroom')
@login_required
@role_required('Participant')
def showroom():
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get user points
    cur.execute("SELECT points FROM users WHERE id = %s", (user_id,))
    points_data = cur.fetchone()
    points = points_data['points'] if points_data else 0
    
    # Get user badges
    cur.execute("""
        SELECT b.*, ub.earned_at FROM badges b 
        JOIN user_badges ub ON b.id = ub.badge_id 
        WHERE ub.user_id = %s
        ORDER BY ub.earned_at DESC
    """, (user_id,))
    badges = cur.fetchall()
    
    # Calculate Rank
    cur.execute("SELECT COUNT(*) as count FROM users WHERE points > %s AND role = 'Participant'", (points,))
    higher_users = cur.fetchone()['count']
    rank = higher_users + 1
    
    cur.close()
    return render_template('participant/showroom.html', 
                           points=points, 
                           badges=badges,
                           rank=rank)
