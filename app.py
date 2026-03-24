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

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    mysql.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.employee import employee_bp
    from routes.participant import participant_bp
    from routes.graph_auth import graph_auth_bp
    from routes.google_auth import google_auth_bp

    from routes.ai_assistant import ai_assistant_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(employee_bp, url_prefix='/employee')
    app.register_blueprint(participant_bp, url_prefix='/participant')
    app.register_blueprint(graph_auth_bp, url_prefix='/microsoft')
    app.register_blueprint(google_auth_bp, url_prefix='/google')
    app.register_blueprint(ai_assistant_bp, url_prefix='/ai')

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
        return render_template('index.html')

    @app.route('/import-db')
    def run_import():
        import os
        from import_db import import_db
        
        # Create a debug report of what variables the app actually sees
        debug_report = "<h3>Debug Report (Environment Variables):</h3><ul>"
        for k, v in os.environ.items():
            if 'MYSQL' in k:
                # Mask password but show length
                val = v if 'PASS' not in k else f"*** (length: {len(v)})"
                debug_report += f"<li><b>{k}</b>: {val}</li>"
        debug_report += "</ul>"

        try:
            import_db()
            return f"<h1>SUCCESS!</h1>{debug_report}<p>Database migration completed successfully. You can now <a href='/auth/login'>Login here</a>.</p>"
        except Exception as e:
            return f"<h1>MIGRATION FAILED</h1><p>Error: {str(e)}</p>{debug_report}<p>Check your Environment Variables in Render!</p>"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5007, debug=False)
