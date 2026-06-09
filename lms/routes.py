from flask import Blueprint, render_template, request, session, abort
from database import *
from utils.encrypt import (
    encrypt_lms_id, decrypt_lms_id, decrypt_user_id, decrypt_skill_id, encrypt_skill_id, slugify
)
from jobs.routes import login_required

lms_bp = Blueprint("lms", __name__)

@lms_bp.route("/learn/<int:skill_id>")
@login_required
def start_learning(skill_id):
    course = get_mandatory_course_by_skill(skill_id)
    chapters = get_chapters_by_course(course["id"])

    for i, ch in enumerate(chapters):
        if i == 0:
            ch["unlocked"] = True
        else:
            prev = chapters[i-1]
            ch["unlocked"] = is_chapter_quiz_passed(
                session["user_id"], prev["id"]
            )

    return render_template(
        "learning_dashboard.html",
        course=course,
        chapters=chapters
    )

@lms_bp.route("/lesson/<int:lesson_id>/watch", methods=["POST"])
@login_required
def watch_lesson(lesson_id):
    mark_lesson_watched(session["user_id"], lesson_id)
    return {"status": "ok"}

@lms_bp.route(
    "/quiz/<string:enc_uid>/<string:course_slug>/<string:enc_course_id>/chapter/quiz/<string:enc_chapter_id>"
)
@login_required
def chapter_quiz(enc_uid, course_slug, enc_course_id, enc_chapter_id):

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    if not course_id:
        abort(404)

    chapter_id = decrypt_lms_id(enc_chapter_id)
    if not chapter_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    if slugify(course["title"]) != course_slug:
        abort(404)

    if not is_chapter_completed(user_id, chapter_id):
        abort(403)

    quiz = get_chapter_quiz(course_id, chapter_id)
    if not quiz:
        abort(404)

    quiz["enc_id"] = encrypt_lms_id(quiz["id"])

    questions = get_quiz_questions(quiz["id"])

    return render_template(
        "chapter_quiz.html",
        quiz=quiz,
        questions=questions,
        enc_uid=enc_uid,
        enc_course_id=enc_course_id,
        enc_chapter_id=enc_chapter_id,
        course_slug=course_slug
    )

@lms_bp.route(
    "/quiz/<string:enc_uid>/<string:course_slug>/<string:enc_course_id>/chapter/quiz/<string:enc_chapter_id>/submit/<string:enc_quiz_id>",
    methods=["POST"]
)
@login_required
def submit_chapter_quiz(enc_uid, course_slug, enc_course_id, enc_chapter_id, enc_quiz_id):

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    chapter_id = decrypt_lms_id(enc_chapter_id)
    quiz_id = decrypt_lms_id(enc_quiz_id)

    if not course_id or not chapter_id or not quiz_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course or slugify(course["title"]) != course_slug:
        abort(404)

    if not is_chapter_completed(user_id, chapter_id):
        abort(403)

    answers = request.form.to_dict()

    score, passed = submit_quiz(
        user_id,
        quiz_id,
        answers
    )

    course_row = get_course_by_id(course_id)
    course = dict(course_row)

    course["slug"] = slugify(course["title"])
    course["enc_skill_id"] = encrypt_skill_id(course["skill_id"])
    course["enc_id"] = encrypt_lms_id(course["id"])


    course["slug"] = slugify(course["title"])
    course["enc_skill_id"] = encrypt_skill_id(course["skill_id"])
    course["enc_id"] = encrypt_lms_id(course["id"])


    return render_template(
        "quiz_result.html",
        score=score,
        passed=passed,
        course=course
    )

@lms_bp.route(
    "/learn/<string:enc_uid>/<string:course_slug>/<string:enc_course_id>/chapter/<string:enc_chapter_id>"
)
@login_required
def chapter_lessons(enc_uid, course_slug, enc_course_id, enc_chapter_id):

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    if not course_id:
        abort(404)

    chapter_id = decrypt_lms_id(enc_chapter_id)
    if not chapter_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    if slugify(course["title"]) != course_slug:
        abort(404)

    lessons = get_lessons_by_chapter(chapter_id)

    for lesson in lessons:
        lesson["enc_id"] = encrypt_lms_id(lesson["id"])
        lesson["watched"] = is_lesson_watched(user_id, lesson["id"])

    chapter_completed = is_chapter_completed(user_id, chapter_id)

    return render_template(
        "chapter_lessons.html",
        lessons=lessons,
        chapter_completed=chapter_completed,
        enc_chapter_id=enc_chapter_id,
        enc_course_id=enc_course_id,
        course_slug=course_slug,
        enc_uid=enc_uid
    )

@lms_bp.route("/lesson/<int:lesson_id>/watched", methods=["POST"])
@login_required
def lesson_watched(lesson_id):

    data = request.get_json()

    if not data or not data.get("video_completed"):
        return {"status": "error", "message": "Video not completed"}, 400

    mark_lesson_watched(session["user_id"], lesson_id)
    return {"status": "ok"}


@lms_bp.route(
    "/quiz/<string:enc_uid>/<string:course_slug>/<string:enc_course_id>/final"
)
@login_required
def final_quiz(enc_uid, course_slug, enc_course_id):

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    if not course_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    if slugify(course["title"]) != course_slug:
        abort(404)

    if not all_chapter_quizzes_passed(user_id, course_id):
        abort(403)

    quiz = get_final_quiz(course_id)
    if not quiz:
        abort(404)

    quiz["enc_id"] = encrypt_lms_id(quiz["id"])

    questions = get_quiz_questions(quiz["id"])

    return render_template(
        "final_quiz.html",
        quiz=quiz,
        questions=questions,
        enc_uid=enc_uid,
        enc_course_id=enc_course_id,
        course_slug=course_slug,
    )

@lms_bp.route(
    "/quiz/<string:enc_uid>/<string:course_slug>/<string:enc_course_id>/final/submit/<string:enc_quiz_id>",
    methods=["POST"]
)
@login_required
def submit_final_quiz(enc_uid, course_slug, enc_course_id, enc_quiz_id):

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    quiz_id = decrypt_lms_id(enc_quiz_id)

    if not course_id or not quiz_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    if slugify(course["title"]) != course_slug:
        abort(404)

    if not all_chapter_quizzes_passed(user_id, course_id):
        abort(403)

    answers = request.form.to_dict()
    score, passed = submit_quiz(user_id, quiz_id, answers)

    if passed and course["course_type"] == "mandatory":
        verify_skill(user_id, course["skill_id"])

    return render_template(
        "final_quiz_result.html",
        score=score,
        passed=passed
    )

def can_access_course(plan_code, course_type):
    """
    plan_code: None | '01' | '02'
    course_type: 'open' | 'mandatory'
    """

    # 🌍 Open courses → everyone
    if course_type == "open":
        return True

    # 🔒 Mandatory → only Elite (02)
    if course_type == "mandatory":
        return plan_code == "02"

    return False


@lms_bp.route("/learning-source/<string:enc_id>")
@login_required
def learning_source(enc_id):

    user_id = decrypt_user_id(enc_id)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    skill = get_skill_by_id(1)
    if not skill:
        abort(404)

    subscribed = get_active_subscription(user_id)
    plan_code = subscribed["plan_code"] if subscribed else None

    raw_courses = get_all_courses()
    all_courses = []

    for row in raw_courses:
        course = dict(row)

        # 🔐 access check
        course["is_locked"] = not can_access_course(
            plan_code,
            course["course_type"]
        )

        course["enc_id"] = encrypt_lms_id(course["id"])
        course["slug"] = slugify(course["title"])
        course["progress"] = get_course_progress(user_id, course["id"])

        all_courses.append(course)

    return render_template(
        "learning_source.html",
        all_courses=all_courses,
        plan_code=plan_code
    )


@lms_bp.route("/lms/start/<string:enc_uid>/<string:course_slug>/<string:enc_skill_id>/<string:enc_course_id>")
@login_required
def start_course(enc_uid, enc_skill_id, course_slug, enc_course_id):

    skill_id = decrypt_skill_id(enc_skill_id)
    if not skill_id:
        abort(404)

    skill = get_skill_by_id(skill_id)
    if not skill:
        abort(404)

    user_id = decrypt_user_id(enc_uid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    course_id = decrypt_lms_id(enc_course_id)
    if not course_id:
        abort(404)

    course = get_course_by_id(course_id)
    if not course:
        abort(404)

    if slugify(course["title"]) != course_slug:
        abort(404)

    chapters = get_chapters_by_course(course_id)

    for i, ch in enumerate(chapters):
        if i == 0:
            ch["unlocked"] = True
        else:
            prev = chapters[i - 1]
            ch["unlocked"] = is_chapter_quiz_passed(
                user_id, prev["id"]
            )

    final_unlocked = all_chapter_quizzes_passed(
        user_id, course_id
    )

    quiz = get_final_quiz(course_id)
    if not quiz:
        abort(404)

    quiz["enc_id"] = encrypt_lms_id(quiz["id"])

    progress = get_course_progress(user_id, course_id)

    print("COURSE ID:", course_id)
    print("CHAPTERS:", chapters)


    return render_template(
        "lms_dashboard.html",
        skill=skill,
        quiz=quiz,
        course=course,
        chapters=chapters,
        progress=progress,
        final_unlocked=final_unlocked
    )
