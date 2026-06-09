from flask import Blueprint, render_template
from utils.encrypt import encrypt_user_id, encrypt_lms_id, encrypt_skill_id
from jobs.routes import login_required


main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.app_context_processor
def inject_encrypt_helpers():
    return {
        "encrypt_user_id": encrypt_user_id,
        "encrypt_lms_id": encrypt_lms_id,
        "encrypt_skill_id": encrypt_skill_id
    }
