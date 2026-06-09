from flask import Blueprint, render_template, session, make_response, abort
from weasyprint import HTML
import uuid

from database import (
    get_certificate,
    create_certificate,
    get_certificate_by_id,
    is_course_completed,
    get_user_by_id,
    get_course_by_id
)

certificate_bp = Blueprint("certificate", __name__)

@certificate_bp.route("/certificate/download/<int:course_id>")
def download_certificate(course_id):
    user_id = session.get("user_id")

    # if not user_id:
    #     abort(401)

    # if not is_course_completed(user_id, course_id):
    #     abort(403)

    # ✅ FIX HERE
    cert = get_certificate(user_id, course_id)

    if not cert:
        certificate_id = f"INV-{uuid.uuid4().hex[:10].upper()}"
        issued_on = create_certificate(user_id, course_id, certificate_id)
    else:
        certificate_id = cert["certificate_id"]
        issued_on = cert["issued_on"]

    return render_template(
        "certificate.html",
        user=get_user_by_id(user_id),
        course=get_course_by_id(course_id),
        certificate_id=certificate_id,
        issued_on=issued_on.strftime("%d %B %Y")
    )

    # pdf = HTML(string=html).write_pdf()

    # response = make_response(pdf)
    # response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = (
    #     f'attachment; filename="Invinsource-Certificate-{course_id}.pdf"'
    # )

    # return response


@certificate_bp.route("/verify/<certificate_id>")
def verify_certificate(certificate_id):
    cert = get_certificate_by_id(certificate_id)

    # if not cert:
    #     abort(404)

    return render_template("verify.html", cert=cert)
