from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from functools import wraps
from database import *
from utils.encrypt import encrypt_id, decrypt_id
from config import UPLOAD_FOLDER
import os

jobs_bp = Blueprint("jobs", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to be logged in....", "error")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@jobs_bp.route("/job")
@jobs_bp.route("/job/<string:enc_id>")
def render_job_page(enc_id=None):

    raw_jobs = load_job_from_db()

    jobs = []
    for job in raw_jobs:
        job_dict = dict(job)
        job_dict["requirements_list"] = [
            s.strip() for s in job_dict["requirements"].split(",")
        ]
        job_dict["responsibilities_list"] = [
            s.strip() for s in job_dict["responsibilities"].split(",")
        ] if job_dict["responsibilities"] else []

        job_dict["enc_id"] = encrypt_id(job_dict["id"])

        jobs.append(job_dict)

    job_detail = None

    if enc_id:
        real_id = decrypt_id(enc_id)
        if not real_id:
            abort(404)

        job_detail = load_job_by_id(real_id)
        if not job_detail:
            abort(404)

        job_detail = dict(job_detail)
        job_detail["requirements_list"] = [
            s.strip() for s in job_detail["requirements"].split(",")
        ]
        job_detail["responsibilities_list"] = [
            s.strip() for s in job_detail["responsibilities"].split(",")
        ] if job_detail["responsibilities"] else []

        job_detail["enc_id"] = enc_id

    if job_detail is None and jobs:
        job_detail = jobs[0]

    applied = False
    if session.get("user_id") and job_detail:
        applied = has_applied(session["user_id"], job_detail["id"])

    return render_template(
        "job.html",
        jobs=jobs,
        job_detail=job_detail,
        applied=applied
    )

@jobs_bp.route("/job-application/<string:enc_id>", methods=["GET", "POST"])
@login_required
def job_application(enc_id):

    job_id = decrypt_id(enc_id)
    if not job_id:
        abort(404)

    job = load_job_by_id(job_id)
    if not job:
        abort(404)

    user_id = session["user_id"]
    user_info = get_user_by_id(user_id)
    user_profile = get_user_profile(user_id)
    

    if request.method == "GET":
        return render_template("apply_job.html", 
                                job=job,
                                user_info=user_info,
                                user_profile=user_profile
                                )

    full_name = request.form.get("name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")

    portfolio_url = request.form.get("portfolio", "").strip() or "N/A"
    github_url = request.form.get("github", "").strip() or "N/A"
    linkedin_url = request.form.get("linkedin", "").strip() or "N/A"
    cover_letter = request.form.get("cover_letter", "").strip() or "N/A"

    experience_years = request.form.get("experience", "").strip()
    experience_years = int(experience_years) if experience_years.isdigit() else 0

    expected_salary = request.form.get("expected_salary", "").strip()
    expected_salary = int(expected_salary) if expected_salary.isdigit() else 0

    resume_file = request.files.get("resume")

    if not resume_file or resume_file.filename == "":
        flash("Resume is required", "error")
        return redirect(request.url)

    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(resume_file.filename):
        flash("Only PDF/DOC/DOCX allowed", "error")
        return redirect(request.url)

    filename = secure_filename(f"{user_id}_{job_id}_{resume_file.filename}")
    resume_path = os.path.join(UPLOAD_FOLDER, filename)
    resume_file.save(resume_path)

    resume_url = f"/{resume_path}"

    try:
        load_application_form_in_db(
            job_id=job_id,
            user_id=user_id,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            resume_url=resume_url,
            portfolio_url=portfolio_url,
            linkedin_url=linkedin_url,
            github_url=github_url,
            cover_letter=cover_letter,
            experience_years=experience_years,
            expected_salary=expected_salary
        )
    except IntegrityError:
        flash("You have already applied for this job", "error")
        return redirect(request.url)

    flash("Application submitted successfully", "success")
    return redirect(url_for("jobs.render_job_page", enc_id=enc_id))
