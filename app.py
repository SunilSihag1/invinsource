from flask import Flask
from config import FLASK_SECRET_KEY
from auth.routes import auth_bp
from jobs.routes import jobs_bp
from dashboard.routes import dashboard_bp
from assignments.routes import assignments_bp
from lms.routes import lms_bp
from main.routes import main_bp
from payment.routes import payment_bp
from user_profile.routes import user_profile_bp
from super_admin.routes import super_admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(lms_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(super_admin_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
