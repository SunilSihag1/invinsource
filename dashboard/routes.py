from flask import Blueprint, render_template, session, abort, request
from database import *
from utils.encrypt import decrypt_user_id, encrypt_lms_id, slugify, encrypt_skill_id
from jobs.routes import login_required
from math import ceil

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/<string:enc_uid>")
@login_required
def dashboard(enc_uid):

    user_id = decrypt_user_id(enc_uid)
    if not user_id:
        abort(404)

    if user_id != session.get("user_id"):
        abort(403)

    user = get_user_dashboard_basic(user_id)
    job_stats = get_job_application_stats(user_id)

    user_skills = get_user_rows_and_count(user_id)

    skill_count = user_skills["count"]

    # sirf skill_id nikal lo
    skill_ids = [row.skill_id for row in user_skills["rows"]]

    # multiple skill names lao
    skill_names = get_skills_by_ids(skill_ids)

    return render_template(
        "user_dashboard.html",
        user=user,
        job_stats=job_stats,
        skill_count=skill_count,
        skill_names=skill_names
    )

@dashboard_bp.route("/profile/applied-application/<string:enc_uid>/")
@login_required
def applied_applications(enc_uid):

    user_id = decrypt_user_id(enc_uid)
    if user_id != session.get("user_id"):
        abort(403)

    # ---- QUERY PARAMS ----
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    app_type = request.args.get("type") 
    status = request.args.get("status")
    search = request.args.get("search", "").strip()

    # ---- FETCH DATA ----
    jobs, job_count = get_applied_jobs(
        user_id, status, search, offset, per_page
    ) if app_type in (None, "job") else ([], 0)

    assignments, assignment_count = get_applied_assignments(
        user_id, status, search, offset, per_page
    ) if app_type in (None, "assignment") else ([], 0)

    combined = jobs + assignments
    combined.sort(key=lambda x: x["applied_at"], reverse=True)

    total = job_count + assignment_count
    total_pages = ceil(total / per_page)

    return render_template(
        "applied_applications.html",
        applications=combined,
        page=page,
        total_pages=total_pages,
        enc_uid=enc_uid
    )



def build_user_courses_with_progress(user_id, raw_courses, status=None):
    """
    raw_courses: list from get_user_courses_raw
    status: completed | in_progress | None
    """
    courses = []

    for course in raw_courses:
        progress = get_course_progress(user_id, course["id"])

        if status == "completed" and progress != 100:
            continue

        if status == "in_progress" and not (0 < progress < 100):
            continue

        courses.append({
            "id": course["id"],
            "title": course["title"],
            "progress": progress
        })

    return courses


# ================= USER COURSES =================
@dashboard_bp.route("/profile/courses/<string:enc_uid>/")
@login_required
def user_courses(enc_uid):

    # -------- SECURITY --------
    user_id = decrypt_user_id(enc_uid)
    if not user_id:
        abort(404)

    if user_id != session.get("user_id"):
        abort(403)

    # -------- QUERY PARAMS --------
    page = int(request.args.get("page", 1))
    per_page = 6
    offset = (page - 1) * per_page

    status = request.args.get("status")        # completed | in_progress | None
    search = request.args.get("search", "").strip()

    # -------- FETCH RAW COURSES (DB) --------
    raw_courses = get_user_courses_raw(
        user_id=user_id,
        search=search,
        offset=offset,
        limit=per_page
    )

    total_courses = get_user_courses_count(
        user_id=user_id,
        search=search
    )

    # -------- BUILD FINAL COURSE LIST --------
    courses = build_user_courses_with_progress(
        user_id=user_id,
        raw_courses=raw_courses,
        status=status
    )

    total_pages = ceil(total_courses / per_page)

    all_courses = []

    if courses:
        for row in courses:
            course = dict(row)

        skill_id = get_skill_id(course["id"])

        course["enc_id"] = encrypt_lms_id(course["id"])
        course["slug"] = slugify(course["title"])
        course["skill_id"] = encrypt_skill_id(skill_id["skill_id"])

        all_courses.append(course)


    return render_template(
        "user_courses.html",
        courses=courses,
        page=page,
        all_courses = all_courses,
        total_pages=total_pages,
        enc_uid=enc_uid
    )
