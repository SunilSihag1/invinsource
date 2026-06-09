from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from database import *
from utils.mailer import send_mail
from config import EMAIL_USER, EMAIL_PASS
import random
import time

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        mail_id = request.form["email"]
        password = request.form["password"]

        users = get_user_data_from_db(mail_id)

        if not users:
            flash("Email is not registered, please signup", "error")
            return redirect(url_for("auth.login"))
        
        if not check_password_hash(users["password_hash"], password):
            flash("Email id or password is incorrect", "error")
            return redirect(url_for("auth.login"))
        
        session.clear()
        session["user_id"] = users["id"]
        session["user_name"] = users["name"]
        session["role"] = users["role"]

        if users["role"] == "super_admin":
            flash("Logged in successfully as super admin", "success")
            return redirect("/super-admin/dashboard")
        elif users["role"] == "admin":
            flash("Logged in successfully as admin", "success")
            return redirect("/")
        else:
            flash("Logged in successfully", "success")
            return redirect(url_for("main.home"))
        
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Password do not match", "error")
            return redirect(url_for("auth.signup"))
        else:
            try:
                hashed_password = generate_password_hash(password)
                create_user_in_db(username, name, email, phone_number, hashed_password)
                flash("Successfully signed up!!!", "success")
                return redirect(url_for("auth.login"))
            except(IntegrityError):
                flash("mail id or username already exist", "error")
        
    return render_template("signup.html")

@auth_bp.route("/forgot-password", methods=["POST", "GET"])
def render_forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = get_user_data_from_db(email)

        if not user:
            flash("Email not registered", "error")
            return redirect(url_for("auth.render_forgot_password"))
        
        otp = random.randint(100000, 999999)
        session["otp"] = otp
        session["otp_mail"] = email
        session["otp_expiry"] = time.time() + 120

        mail_subject = "Your OTP Verification Code"
        mail_content = f"Your OTP is: {otp}\nThis OTP is valid for 2 minutes."

        send_mail(email, mail_subject, mail_content)
        return redirect(url_for("auth.render_otp_verification"))

    return render_template("forgot_password.html")

@auth_bp.route("/otp-verification", methods=["GET", "POST"])
def render_otp_verification():
    if request.method == "POST":
        user_otp = request.form["otp"]

        if time.time() > session.get("otp_expiry", 0):
            flash("OTP expired. Please try again.", "error")
            session.clear()
            return redirect(url_for("auth.render_forgot_password"))

        if "otp" not in session:
            flash("Session expired. Try again.", "error")
            return redirect(url_for("auth.render_forgot_password"))

        session["otp_verified"] = True
        return redirect(url_for("auth.render_reset_password"))

    return render_template("otp_verification.html")

@auth_bp.route("/reset-password", methods=["GET", "POST"])
def render_reset_password():
    if not session.get("otp_verified"):
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(request.url)

        hashed = generate_password_hash(password)
        email = session["otp_mail"]

        with engine.begin() as conn:
            conn.execute(
                text("UPDATE users SET password_hash=:pwd WHERE email=:email"),
                {"pwd": hashed, "email": email}
            )

        session.clear()
        flash("Password reset successfully", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html")
