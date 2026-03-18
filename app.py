from flask import Flask, redirect, url_for, session
from config import Config
from utils.db import MySQL
import os

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(f"DEBUG: MYSQL_HOST={app.config.get('MYSQL_HOST')}")
    print(f"DEBUG: MYSQL_USER={app.config.get('MYSQL_USER')}")
    print(f"DEBUG: MYSQL_DB={app.config.get('MYSQL_DB')}")

    mysql.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.employee import employee_bp
    from routes.participant import participant_bp
    from routes.graph_auth import graph_auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(employee_bp, url_prefix='/employee')
    app.register_blueprint(participant_bp, url_prefix='/participant')
    app.register_blueprint(graph_auth_bp, url_prefix='/microsoft')

    @app.route('/')
    def index():
        if 'user_id' in session:
            role = session.get('role')
            if role == 'Admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'Employee':
                return redirect(url_for('employee.dashboard'))
            elif role == 'Participant':
                return redirect(url_for('participant.dashboard'))
        from flask import render_template
        return render_template('landing.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5001)
