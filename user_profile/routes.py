from flask import Blueprint, render_template, abort, session, request, flash, redirect, url_for
from utils.encrypt import decrypt_user_id
from jobs.routes import login_required
from database import get_user_by_id, get_skills_by_ids, get_user_rows_and_count, upsert_user_profile, update_user_basic_info, update_resume_url, get_user_profile, get_all_skills, get_user_skills, sync_user_skills, get_unverified_skill, get_skill_progress
import os
from werkzeug.utils import secure_filename


user_profile_bp = Blueprint("user_profile", __name__)

UPLOAD_FOLDER = "uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf"}

@user_profile_bp.route("/profile/<string:enc_uid>")
@login_required
def render_profile_page(enc_uid):
    user_id = decrypt_user_id(enc_uid)
    if not user_id:
        abort(404)

    if user_id != session.get("user_id"):
        abort(403)  

    user_info = get_user_by_id(user_id)
    user_skills = get_user_rows_and_count(user_id)
    user_profile = get_user_profile(user_id)
    all_skills = get_all_skills()  # master skills
    user_skill_ids = get_user_skills(user_id)  # [1, 3, 5]
    unverified_skills = get_unverified_skill(user_id)
    skill_progress = get_skill_progress(user_id)


    skill_ids = [row.skill_id for row in user_skills["rows"]]
    skill_names = get_skills_by_ids(skill_ids)


    return render_template(
        "user_profile.html",
        user_info=user_info,
        skill_names=skill_names,
        all_skills=all_skills,
        user_skill_ids=user_skill_ids,
        user_profile=user_profile,
        unverified_skills=unverified_skills,
        skill_progress=skill_progress,
        enc_uid=enc_uid
        )

@user_profile_bp.route("/profile/update/<string:enc_uid>", methods=["POST", "GET"])
@login_required
def update_profile(enc_uid):
    user_id = decrypt_user_id(enc_uid)

    if not user_id or user_id != session.get("user_id"):
        abort(403)

    # -------- USERS TABLE DATA --------
    username = request.form.get("username").strip()
    email = request.form.get("email").strip()
    phone = request.form.get("phone_number").strip()

    update_user_basic_info(
        user_id=user_id,
        username=username,
        email=email,
        phone_number=phone
    )

    # -------- USER_PROFILES TABLE DATA --------
    bio = request.form.get("bio")
    education = request.form.get("education")
    experience_level = request.form.get("experience_level")
    github_url = request.form.get("github_url")
    linkedin_url = request.form.get("linkedin_url")
    selected_skills = request.form.getlist("skills")  # ['1', '3', '5']
    selected_skills = set(map(int, selected_skills))

    sync_user_skills(user_id, selected_skills)



    upsert_user_profile(
        user_id=user_id,
        bio=bio,
        education=education,
        experience_level=experience_level,
        github_url=github_url,
        linkedin_url=linkedin_url,
    )

    flash("Profile updated successfully", "success")
    return redirect(url_for("user_profile.render_profile_page", enc_uid=enc_uid))

@user_profile_bp.route("/profile/upload-resume/<string:enc_uid>", methods=["POST"])
@login_required
def upload_resume(enc_uid):

    user_id = decrypt_user_id(enc_uid)
    if user_id != session.get("user_id"):
        abort(403)

    file = request.files.get("resume")

    if not file or "." not in file.filename:
        flash("Invalid file", "error")
        return redirect(request.referrer)

    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        flash("Only PDF allowed", "error")
        return redirect(request.referrer)

    filename = secure_filename(f"{user_id}_resume.pdf")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Save URL in DB
    update_resume_url(user_id, f"/{UPLOAD_FOLDER}/{filename}")

    flash("Resume uploaded successfully", "success")
    return redirect(request.referrer)