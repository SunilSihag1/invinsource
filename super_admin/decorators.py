from functools import wraps
from flask import session, redirect, url_for, abort

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

        if session.get("role") != "super_admin":
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
