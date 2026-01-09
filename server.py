# server.py
from flask import Flask, render_template, redirect, session
import os
from dotenv import load_dotenv
load_dotenv()

from backend.db import get_connection, close_connection
import backend.data_manager as data_manager
from backend.api import api_bp
import backend.auth as auth
import backend.scheduler as scheduler
from backend.pdf_api import pdf_bp

# 🔐 IMPORT DECORATORS DIRECTLY (FIX)
from backend.auth import login_required, admin_required, user_required

app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_folder='frontend/static'
)

# Set secret key for sessions
app.secret_key = os.environ.get(
    'SECRET_KEY',
    'your-secret-key-change-this-in-production-2024'
)

# ================== REGISTER BLUEPRINTS ==================

app.register_blueprint(data_manager.bp)
app.register_blueprint(api_bp)
app.register_blueprint(scheduler.bp)
app.register_blueprint(pdf_bp)
app.register_blueprint(auth.bp, url_prefix='/auth')

# ================== TEMPLATE CONTEXT ==================

@app.context_processor
def inject_user_role():
    """Make user role available in all templates"""
    if 'user_id' in session:
        return {
            'is_admin': session.get('role') == 'admin',
            'current_user': session.get('username'),
            'user_role': session.get('role')
        }
    return {
        'is_admin': False,
        'current_user': None,
        'user_role': None
    }

# ================== MAIN ROUTES ==================

@app.route('/')
@login_required
def home():
    return render_template('review1.html')

@app.route('/review<int:review_num>')
@app.route('/review/<int:review_num>')
@login_required
def review_page(review_num):
    if 0 <= review_num <= 5:
        return render_template(f'review{review_num}.html')
    return redirect("/")

@app.route('/data-manager')
@admin_required
def data_manager_page():
    """Only admins can access data manager"""
    return render_template('data-manager.html')

@app.route('/pdf-viewer')
@admin_required
def pdf_viewer_page():
    return render_template('pdf_viewer.html')

# ================== ERROR HANDLERS ==================

@app.errorhandler(404)
def not_found_error(error):
    if 'user_id' not in session:
        return redirect('/auth/login')
    return render_template('review1.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal Server Error"}, 500

# ================== SCHEDULER ROUTES ==================

@app.route('/scheduler')
@admin_required
def scheduler_page():
    return render_template('scheduler.html')

# ================== ATTENDANCE DASHBOARD ==================

@app.route('/attendance-dashboard')
@login_required
def attendance_dashboard():
    return render_template('attendance-dashboard.html')

# ================== FINAL SHEET ==================

@app.route('/final-sheet')
@login_required
def final_sheet_page():
    return render_template('final_sheet.html')

# ================== APPLICATION STARTUP ==================

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'


    # Optional DB connection test
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print(f"✅ Connected to database: {db[0]}")
        close_connection(conn)
    else:
        print("❌ Database connection failed at startup!")

    print(f"🚀 Server running on {host}:{port}")
    print(f"🔐 Login at: http://{host}:{port}/auth/login")

    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
