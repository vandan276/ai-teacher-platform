from utils.db import get_db

def award_points(user_id, points):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET points = points + %s WHERE id = %s", (points, user_id))
    db.commit()

def check_and_award_badges(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 1. Quick Starter (1st module)
    cursor.execute("SELECT COUNT(*) as count FROM progress WHERE user_id = %s AND completed = TRUE", (user_id,))
    completed_count = cursor.fetchone()['count']
    if completed_count >= 1:
        award_badge_by_criteria(user_id, 'quick_start')
    
    # 2. AI Explorer (3rd module)
    if completed_count >= 3:
        award_badge_by_criteria(user_id, 'ai_explorer')
        
    # 3. Master Educator (All modules)
    cursor.execute("SELECT COUNT(*) as total FROM modules")
    total_modules = cursor.fetchone()['total']
    if completed_count >= total_modules and total_modules > 0:
        award_badge_by_criteria(user_id, 'master_educator')

def award_badge_by_criteria(user_id, criteria):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM badges WHERE criteria = %s", (criteria,))
    badge = cursor.fetchone()
    if badge:
        cursor.execute("INSERT IGNORE INTO user_badges (user_id, badge_id) VALUES (%s, %s)", (user_id, badge['id']))
        db.commit()
