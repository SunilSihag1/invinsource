from flask import Blueprint, render_template
from .decorators import super_admin_required

super_admin_bp = Blueprint(
    "super_admin",
    __name__,
    url_prefix="/super-admin"
)

@super_admin_bp.route("/dashboard")
@super_admin_required
def dashboard():
    stats = {
        "users": 120,
        "courses": 15,
        "payments": 342,
        "revenue": 98500
    }
    return render_template("super_admin/dashboard.html", stats=stats)