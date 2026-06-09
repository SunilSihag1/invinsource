from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from database import *
from utils.encrypt import encrypt_id, decrypt_id
from jobs.routes import login_required
from sqlalchemy.exc import IntegrityError

assignments_bp = Blueprint("assignments", __name__)

@assignments_bp.route("/assignments")
@assignments_bp.route("/assignments/<string:enc_id>")
@login_required
def render_assignment_page(enc_id=None):

    raw_assignments = load_assignments_from_db()

    assignments = []
    for a in raw_assignments:
        a["skills_list"] = [
            s.strip() for s in (a.get("skills") or "").split(",") if s
        ]

        a["deliverables_list"] = [
            d.strip() for d in (a.get("deliverables") or "").split(",") if d
        ]

        a["enc_id"] = encrypt_id(a["id"])
        assignments.append(a)

    assignment_detail = None

    if enc_id:
        real_id = decrypt_id(enc_id)
        if not real_id:
            abort(404)

        assignment_detail = load_assignment_by_id(real_id)
        if not assignment_detail:
            abort(404)

        assignment_detail["skills_list"] = [
            s.strip() for s in (assignment_detail.get("skills") or "").split(",")
        ]

        assignment_detail["deliverables_list"] = [
            d.strip() for d in (assignment_detail.get("deliverables") or "").split(",")
        ]

        assignment_detail["enc_id"] = enc_id

    if assignment_detail is None and assignments:
        assignment_detail = assignments[0]

    applied = False
    if session.get("user_id") and assignment_detail:
        applied = has_applied_assignment(
            session["user_id"],
            assignment_detail["id"]
        )

    return render_template(
        "assignment.html",
        assignments=assignments,
        assignment_detail=assignment_detail,
        applied=applied
    )

@assignments_bp.route("/assignment-application/<string:enc_id>", methods=["GET", "POST"])
@login_required
def assignment_application(enc_id):

    assignment_id = decrypt_id(enc_id)
    if not assignment_id:
        abort(404)

    assignment = load_assignment_by_id(assignment_id)
    if not assignment:
        abort(404)

    user_id = session["user_id"]
    user_info = get_user_by_id(user_id)
    user_profile = get_user_profile(user_id)

    if has_applied_assignment(user_id, assignment_id):
        flash("You have already applied for this assignment", "error")
        return redirect(url_for("assignments.render_assignment_page", enc_id=enc_id))

    if request.method == "POST":
        insert_assignment_application(
            assignment_id=assignment_id,
            user_id=session["user_id"],
            full_name=request.form["name"],
            email=request.form["email"],
            phone_number=request.form["phone_number"],
            portfolio_url=request.form.get("portfolio"),
            github_url=request.form.get("github"),
            linkedin_url=request.form.get("linkedin"),
            cover_letter=request.form.get("cover_letter")
        )

        flash("Assignment application submitted successfully", "success")
        return redirect(url_for("assignments.render_assignment_page", enc_id=enc_id))

    return render_template(
        "apply_assignment.html",
        assignment=assignment,
        user_info=user_info,
        user_profile=user_profile
    )
