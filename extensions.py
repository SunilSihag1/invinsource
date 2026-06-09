from itsdangerous import URLSafeSerializer
from functools import wraps
from flask import session, redirect

def create_serializers(secret_key):
    return {
        "job": URLSafeSerializer(secret_key, salt="job-id"),
        "user": URLSafeSerializer(secret_key, salt="dashboard-user"),
        "lms": URLSafeSerializer(secret_key, salt="lms-id"),
    }

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper