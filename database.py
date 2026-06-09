from sqlalchemy import create_engine, text
from datetime import datetime

engine = create_engine(
    "mysql+pymysql://root:Sihag%400807@localhost:3306/invinsource?charset=utf8mb4",
    pool_pre_ping=True
)

def create_user_in_db(username, name, email, phone_number, password):
    with engine.begin() as conn:
        conn.execute(text("insert into users(username, name, email, phone_number, password_hash) values(:username, :name, :email, :phone_number, :password_hash)"), {"username" : username, "name" : name, "email" : email, "phone_number" : phone_number, "password_hash" : password}) 

def get_user_data_from_db(mail_id):
    with engine.conNnect() as conn :
        result = conn.execute(text("select * from users where email = :email"), {"email" : mail_id})
        return result.mappings().first()
    
def load_job_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM job"))
        return result.mappings().all()

def load_job_by_id(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from job where id = :id"), {"id": id})
        return result.mappings().first()

from sqlalchemy import text

def load_application_form_in_db(
    job_id,
    user_id,
    full_name,
    email,
    phone_number,
    resume_url,
    portfolio_url,
    linkedin_url,
    github_url,
    cover_letter,
    experience_years,
    expected_salary
):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO job_applications (
                    job_id,
                    user_id,
                    full_name,
                    email,
                    phone_number,
                    resume_url,
                    portfolio_url,
                    linkedin_url,
                    github_url,
                    cover_letter,
                    experience_years,
                    expected_salary
                ) VALUES (
                    :job_id,
                    :user_id,
                    :full_name,
                    :email,
                    :phone_number,
                    :resume_url,
                    :portfolio_url,
                    :linkedin_url,
                    :github_url,
                    :cover_letter,
                    :experience_years,
                    :expected_salary
                )
            """),
            {
                "job_id": job_id,
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "resume_url": resume_url,
                "portfolio_url": portfolio_url,
                "linkedin_url": linkedin_url,
                "github_url": github_url,
                "cover_letter": cover_letter,
                "experience_years": experience_years,
                "expected_salary": expected_salary
            }
        )

def has_applied(user_id, job_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 1 FROM job_applications
                WHERE user_id=:uid AND job_id=:jid
            """),
            {"uid": user_id, "jid": job_id}
        )
        return result.first() is not None

def get_user_dashboard_basic(user_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    u.id,
                    u.name,
                    u.email,
                    COALESCE(up.profile_completed, 0) AS profile_completed
                FROM users u
                LEFT JOIN user_profiles up ON up.user_id = u.id
                WHERE u.id = :uid
            """),
            {"uid": user_id}
        )
    return result.mappings().first()

def get_job_application_stats(user_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    COUNT(*) AS total,
                    SUM(status='shortlisted') AS shortlisted,
                    SUM(status='rejected') AS rejected,
                    SUM(status='hired') AS hired
                FROM job_applications
                WHERE user_id = :uid
            """),
            {"uid": user_id}
        )
    return result.mappings().first()

def get_recent_job_applications(user_id, limit=5):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    j.title,
                    ja.status,
                    ja.applied_at
                FROM job_applications ja
                JOIN job j ON j.id = ja.job_id
                WHERE ja.user_id = :uid
                ORDER BY ja.applied_at DESC
                LIMIT :limit
            """),
            {"uid": user_id, "limit": limit}
        )
    return result.mappings().all()

def get_all_applied_jobs(user_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 
                    j.title,
                    j.location,
                    ja.status,
                    ja.applied_at
                FROM job_applications ja
                JOIN job j ON j.id = ja.job_id
                WHERE ja.user_id = :uid
                ORDER BY ja.applied_at DESC
            """),
            {"uid": user_id}
        )
    return result.mappings().all()

def get_shortlisted_companies(user_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT DISTINCT
                    c.company_name
                FROM job_applications ja
                JOIN job j ON j.id = ja.job_id
                JOIN companies c ON c.id = j.company_id
                WHERE ja.user_id = :uid
                AND ja.status = 'shortlisted'
            """),
            {"uid": user_id}
        )
    return result.mappings().all()


def load_assignments_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM assignments"))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    
def load_assignment_by_id(assignment_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM assignments WHERE id=:id"),
            {"id": assignment_id}
        ).fetchone()

        return dict(result._mapping) if result else None
    
def has_applied_assignment(user_id, assignment_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT 1 FROM assignment_applications
                WHERE user_id=:uid AND assignment_id=:aid
            """),
            {"uid": user_id, "aid": assignment_id}
        ).fetchone()

        return result is not None

def insert_assignment_application(
    assignment_id,
    user_id,
    full_name,
    email,
    phone_number,
    portfolio_url=None,
    github_url=None,
    linkedin_url=None,
    cover_letter=None
):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO assignment_applications
                (
                    assignment_id,
                    user_id,
                    full_name,
                    email,
                    phone_number,
                    portfolio_url,
                    github_url,
                    linkedin_url,
                    cover_letter,
                    application_status
                )
                VALUES
                (
                    :assignment_id,
                    :user_id,
                    :full_name,
                    :email,
                    :phone_number,
                    :portfolio_url,
                    :github_url,
                    :linkedin_url,
                    :cover_letter,
                    'applied'
                )
            """),
            {
                "assignment_id": assignment_id,
                "user_id": user_id,
                "full_name": full_name,
                "email": email,
                "phone_number": phone_number,
                "portfolio_url": portfolio_url or "N/A",
                "github_url": github_url or "N/A",
                "linkedin_url": linkedin_url or "N/A",
                "cover_letter": cover_letter or "N/A"
            }
        )

def get_mandatory_course_by_skill(skill_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM courses
                WHERE skill_id=:sid AND course_type='mandatory'
            """),
            {"sid": skill_id}
        ).fetchone()

        return dict(row._mapping) if row else None

def get_chapters_by_course(course_id):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT * FROM chapters
                WHERE course_id=:cid
                ORDER BY chapter_order
            """),
            {"cid": course_id}
        ).fetchall()

        return [dict(r._mapping) for r in rows]

def get_lessons_by_chapter(chapter_id):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT * FROM lessons
                WHERE chapter_id=:cid
                ORDER BY lesson_order
            """),
            {"cid": chapter_id}
        ).fetchall()

        return [dict(r._mapping) for r in rows]

def mark_lesson_watched(user_id, lesson_id):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO user_lesson_progress (user_id, lesson_id, watched, watched_at)
                VALUES (:uid, :lid, 1, NOW())
                ON DUPLICATE KEY UPDATE watched=1, watched_at=NOW()
            """),
            {"uid": user_id, "lid": lesson_id}
        )

def is_chapter_completed(user_id, chapter_id):
    with engine.connect() as conn:
        total = conn.execute(
            text("SELECT COUNT(*) FROM lessons WHERE chapter_id=:cid"),
            {"cid": chapter_id}
        ).scalar()

        watched = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM user_lesson_progress ulp
                JOIN lessons l ON l.id = ulp.lesson_id
                WHERE ulp.user_id=:uid AND l.chapter_id=:cid AND ulp.watched=1
            """),
            {"uid": user_id, "cid": chapter_id}
        ).scalar()

        return total == watched and total > 0


def get_quiz(quiz_type, course_id, chapter_id=None):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM quizzes
                WHERE quiz_type=:qt
                AND course_id=:cid
                AND (:chid IS NULL OR chapter_id=:chid)
            """),
            {"qt": quiz_type, "cid": course_id, "chid": chapter_id}
        ).fetchone()

        return dict(row._mapping) if row else None

def get_quiz_questions(quiz_id):
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT id, question, option_a, option_b, option_c, option_d
                FROM quiz_questions
                WHERE quiz_id=:qid
            """),
            {"qid": quiz_id}
        ).fetchall()

        return [dict(r._mapping) for r in rows]

def submit_quiz(user_id, quiz_id, answers: dict):
    with engine.connect() as conn:
        questions = conn.execute(
            text("""
                SELECT id, correct_option
                FROM quiz_questions
                WHERE quiz_id=:qid
            """),
            {"qid": quiz_id}
        ).fetchall()

    total = len(questions)
    correct = 0

    for q in questions:
        if answers.get(str(q.id)) == q.correct_option:
            correct += 1

    score = int((correct / total) * 100)
    passed = score >= 80

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO user_quiz_attempts
                (user_id, quiz_id, score_percentage, passed)
                VALUES (:uid, :qid, :score, :passed)
                ON DUPLICATE KEY UPDATE
                score_percentage=:score,
                passed=:passed
            """),
            {
                "uid": user_id,
                "qid": quiz_id,
                "score": score,
                "passed": passed
            }
        )

    return score, passed

def verify_skill_if_eligible(user_id, skill_id, course_id):
    with engine.connect() as conn:
        failed = conn.execute(
            text("""
                SELECT COUNT(*) FROM quizzes q
                LEFT JOIN user_quiz_attempts uqa
                ON q.id = uqa.quiz_id AND uqa.user_id=:uid
                WHERE q.course_id=:cid
                AND (uqa.passed IS NULL OR uqa.passed=0)
            """),
            {"uid": user_id, "cid": course_id}
        ).scalar()

    if failed == 0:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO user_skill_verification (user_id, skill_id, is_verified, verified_at)
                    VALUES (:uid, :sid, 1, NOW())
                    ON DUPLICATE KEY UPDATE
                    is_verified=1,
                    verified_at=NOW()
                """),
                {"uid": user_id, "sid": skill_id}
            )
        return True

    return False

def get_skill_by_id(skill_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM skills WHERE id=:id"),
            {"id": skill_id}
        ).fetchone()
        return dict(row._mapping) if row else None


def is_lesson_watched(user_id, lesson_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT watched
                FROM user_lesson_progress
                WHERE user_id=:uid AND lesson_id=:lid
            """),
            {"uid": user_id, "lid": lesson_id}
        ).fetchone()

        return bool(row and row.watched)

def get_chapter_quiz(course_id, chapter_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM quizzes
                WHERE quiz_type='chapter'
                  AND course_id=:cid
                  AND chapter_id=:chid
            """),
            {"cid": course_id, "chid": chapter_id}
        ).fetchone()

        return dict(row._mapping) if row else None

def all_chapter_quizzes_passed(user_id, course_id):
    with engine.connect() as conn:
        total = conn.execute(
            text("""
                SELECT COUNT(*) FROM quizzes
                WHERE course_id=:cid AND quiz_type='chapter'
            """),
            {"cid": course_id}
        ).scalar()

        passed = conn.execute(
            text("""
                SELECT COUNT(*) 
                FROM quizzes q
                JOIN user_quiz_attempts uqa
                  ON q.id = uqa.quiz_id
                WHERE q.course_id=:cid
                  AND q.quiz_type='chapter'
                  AND uqa.user_id=:uid
                  AND uqa.passed=1
            """),
            {"cid": course_id, "uid": user_id}
        ).scalar()

        return total > 0 and total == passed

def get_final_quiz(course_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM quizzes
                WHERE quiz_type='final'
                  AND course_id=:cid
            """),
            {"cid": course_id}
        ).fetchone()

        return dict(row._mapping) if row else None

def verify_skill(user_id, skill_id):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO user_skill_verification
                (user_id, skill_id, is_verified, verified_at)
                VALUES (:uid, :sid, 1, NOW())
                ON DUPLICATE KEY UPDATE
                    is_verified=1,
                    verified_at=NOW()
            """),
            {"uid": user_id, "sid": skill_id}
        )

def is_chapter_quiz_passed(user_id, chapter_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT uqa.passed
                FROM quizzes q
                JOIN user_quiz_attempts uqa
                  ON q.id = uqa.quiz_id
                WHERE q.quiz_type='chapter'
                  AND q.chapter_id=:chid
                  AND uqa.user_id=:uid
            """),
            {"chid": chapter_id, "uid": user_id}
        ).fetchone()

        return bool(row and row.passed)

def get_next_chapter(course_id, current_order):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM chapters
                WHERE course_id=:cid
                  AND chapter_order > :order
                ORDER BY chapter_order
                LIMIT 1
            """),
            {"cid": course_id, "order": current_order}
        ).fetchone()

        return dict(row._mapping) if row else None

def is_skill_verified(user_id, skill_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT is_verified
                FROM user_skill_verification
                WHERE user_id=:uid AND skill_id=:sid
            """),
            {"uid": user_id, "sid": skill_id}
        ).fetchone()

        return bool(row and row.is_verified)

def get_course_progress(user_id, course_id):
    with engine.connect() as conn:
        total = conn.execute(
            text("""
                SELECT COUNT(*) FROM quizzes
                WHERE course_id = :cid
            """),
            {"cid": course_id}
        ).scalar()

        passed = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM quizzes q
                JOIN user_quiz_attempts uqa
                  ON q.id = uqa.quiz_id
                WHERE q.course_id = :cid
                  AND uqa.user_id = :uid
                  AND uqa.passed = 1
            """),
            {"cid": course_id, "uid": user_id}
        ).scalar()

        # 🔐 SAFETY CHECK (VERY IMPORTANT)
        if not total or total == 0:
            return 0

        percent = int((passed / total) * 100)
        return percent

def get_all_courses():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM courses ORDER BY created_at DESC")
        ).mappings().all()

        return result

def get_course_by_id(course_id):
    with engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM courses WHERE id=:id"),
            {"id": course_id}
        ).mappings().first()

def get_subscriptions_from_db():
    with engine.connect() as conn:
        return conn.execute(
            text("select * from subscriptions")
        ).mappings().all()
    
def get_subscription_by_plan_code(plan_code):
    with engine.connect() as conn:
        return conn.execute(
            text("select * from subscriptions where plan_code = :plan_code"),
            {"plan_code": plan_code}
        ).mappings().first()
    
from sqlalchemy import text

def insert_user_subscription(
    user_id,
    subscription_id,
    start_date,
    end_date,
    amount_paid,
    payment_status,
    subscription_status,
    razorpay_payment_id,
    razorpay_order_id
):
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO user_subscriptions
                    (
                        user_id,
                        subscription_id,
                        start_date,
                        end_date,
                        amount_paid,
                        payment_status,
                        subscription_status,
                        razorpay_payment_id,
                        razorpay_order_id
                    )
                    VALUES
                    (
                        :user_id,
                        :subscription_id,
                        :start_date,
                        :end_date,
                        :amount_paid,
                        :payment_status,
                        :subscription_status,
                        :razorpay_payment_id,
                        :razorpay_order_id
                    )
                """),
                {
                    "user_id": user_id,
                    "subscription_id": subscription_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "amount_paid": amount_paid,
                    "payment_status": payment_status,
                    "subscription_status": subscription_status,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_order_id": razorpay_order_id
                }
            )
            return result.lastrowid
        
    except Exception as e:
        print("❌ DB ERROR (user_subscriptions):", e)
        raise

def insert_payment(
    user_id,
    amount,
    razorpay_payment_id,
    razorpay_order_id,
    razorpay_signature,
    status,
    error_code, 
    error_reason
):

    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO payments
                    (
                        user_id,
                        amount,
                        razorpay_payment_id,
                        razorpay_order_id,
                        razorpay_signature,
                        status,
                        error_code,
                        error_reason
                    )
                    VALUES
                    (
                        :user_id,
                        :amount,
                        :razorpay_payment_id,
                        :razorpay_order_id,
                        :razorpay_signature,
                        :status,
                        :error_code,
                        :error_reason
                    )
                """),
                {
                    "user_id": user_id,
                    "amount": amount,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_signature": razorpay_signature,
                    "status": status,
                    "error_code": error_code,
                    "error_reason": error_reason
                }
            )

            return result.lastrowid

    except Exception as e:
        print("❌ DB ERROR (payments):", e)
        raise

def get_latest_success_payment(user_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT
                    p.razorpay_payment_id,
                    p.amount,
                    p.created_at,
                    s.name AS plan_name,
                    us.start_date,
                    us.end_date
                FROM payments p
                JOIN user_subscriptions us ON us.user_id = p.user_id
                JOIN subscriptions s ON s.id = us.subscription_id
                WHERE p.user_id = :uid
                  AND p.status = 'success'
                ORDER BY p.created_at DESC
                LIMIT 1
            """),       
            {"uid": user_id}
        ).mappings().first()


def get_latest_failed_payment(user_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT
                p.razorpay_payment_id,
                p.amount,
                p.error_code,
                p.error_reason,
                s.plan_code,
                s.name AS plan_name
                FROM payments p
                LEFT JOIN subscriptions s
                ON s.price = p.amount
                WHERE p.user_id = 7
                AND p.status = 'failed'
                ORDER BY p.created_at DESC
                LIMIT 1;
            """),
            {"uid": user_id}
        ).mappings().first()


def get_plan_code_from_plan_name(plan_name):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT plan_code
                FROM subscriptions
                WHERE name = :name
            """),
            {"name": plan_name}
        ).mappings().first()["plan_code"]
    
def get_active_subscription(user_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT s.plan_code
                FROM user_subscriptions us
                JOIN subscriptions s ON s.id = us.subscription_id
                WHERE us.user_id = :uid
                  AND us.subscription_status = 'active'
                  AND us.end_date >= CURDATE()
                ORDER BY us.created_at DESC
                LIMIT 1
            """),
            {"uid": user_id}
        ).mappings().first()



def get_certificate(user_id, course_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT *
                FROM certificates
                WHERE user_id = :uid
                  AND course_id = :cid
                LIMIT 1
            """),
            {"uid": user_id, "cid": course_id}
        ).mappings().first()

def create_certificate(user_id, course_id, certificate_id):
    issued_on = datetime.now()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO certificates (user_id, course_id, certificate_id, issued_on)
                VALUES (:uid, :cid, :cert_id, :issued_on)
            """),
            {
                "uid": user_id,
                "cid": course_id,
                "cert_id": certificate_id,
                "issued_on": issued_on
            }
        )

    return issued_on

def get_certificate_by_id(certificate_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT 
                    c.certificate_id,
                    c.issued_on,
                    c.status,
                    u.name AS user_name,
                    co.title AS course_title
                FROM certificates c
                JOIN users u ON u.id = c.user_id
                JOIN courses co ON co.id = c.course_id
                WHERE c.certificate_id = :cert_id
                LIMIT 1
            """),
            {"cert_id": certificate_id}
        ).mappings().first()

def is_course_completed(user_id, course_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT progress_percentage
                FROM course_progress
                WHERE user_id = :uid
                  AND course_id = :cid
                LIMIT 1
            """),
            {"uid": user_id, "cid": course_id}
        ).mappings().first()

    return row and row["progress_percentage"] == 100

def get_user_by_id(id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                select * from users where id = :user_id
                """),
            {"user_id": id}
        ).mappings().first()
    
def get_user_rows_and_count(user_id):
    with engine.begin() as conn:
        # user ki saari rows
        rows = conn.execute(
            text("SELECT * FROM user_skill_verification WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchall()

        # user kitni baar repeat hua
        count = conn.execute(
            text("SELECT COUNT(*) FROM user_skill_verification WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).scalar()

    return {
        "rows": rows,
        "count": count
    }

def get_skills_by_ids(skill_ids):
    if not skill_ids:
        return []

    placeholders = ",".join([str(i) for i in skill_ids])

    with engine.begin() as conn:
        result = conn.execute(
            text(f"SELECT id, name FROM skills WHERE id IN ({placeholders})")
        ).fetchall()

    return result

def update_user_basic_info(user_id, username, email, phone_number):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE users
            SET username=:username,
                email=:email,
                phone_number=:phone
            WHERE id=:uid
        """), {
            "username": username,
            "email": email,
            "phone": phone_number,
            "uid": user_id
        })

def upsert_user_profile(user_id, bio, education, experience_level,
                        github_url, linkedin_url):

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO user_profiles (
                user_id, bio, education, experience_level,
                github_url, linkedin_url
            ) VALUES (
                :user_id, :bio, :education, :experience_level,
                :github_url, :linkedin_url
            )
            ON DUPLICATE KEY UPDATE
                bio=:bio,
                education=:education,
                experience_level=:experience_level,
                github_url=:github_url,
                linkedin_url=:linkedin_url
        """), locals())

def update_resume_url(user_id, resume_url):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE user_profiles
            SET resume_url=:url
            WHERE user_id=:uid
        """), {"url": resume_url, "uid": user_id})

def get_user_profile(user_id):
    with engine.connect() as conn:
        return conn.execute(text("""
            select * from user_profiles where user_id = :user_id
        """), {"user_id": user_id}).mappings().first()
    
def get_all_skills():
    with engine.connect() as conn:
        return conn.execute(text("SELECT id, name FROM skills")).fetchall()

def get_user_skills(user_id):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT skill_id FROM user_skills WHERE user_id=:uid"),
            {"uid": user_id}
        ).fetchall()
    return [r.skill_id for r in rows]

def sync_user_skills(user_id, selected_skills):
    with engine.begin() as conn:

        # existing skills
        existing = conn.execute(
            text("SELECT skill_id FROM user_skills WHERE user_id=:uid"),
            {"uid": user_id}
        ).fetchall()

        existing_skills = {r.skill_id for r in existing}

        # ADD new skills
        for skill_id in selected_skills - existing_skills:
            conn.execute(text("""
                INSERT INTO user_skills (user_id, skill_id, status)
                VALUES (:uid, :sid, 'pending')
            """), {"uid": user_id, "sid": skill_id})

        # REMOVE unchecked skills
        for skill_id in existing_skills - selected_skills:
            conn.execute(text("""
                DELETE FROM user_skills
                WHERE user_id=:uid AND skill_id=:sid
            """), {"uid": user_id, "sid": skill_id})

def get_unverified_skill(user_id):
    with engine.connect() as conn:
        return conn.execute(
            text("""
                SELECT s.id, s.name
                FROM skills s
                JOIN user_skills us ON us.skill_id = s.id
                WHERE us.user_id = :user_id
                AND us.status = 'pending'
            """),
            {"user_id": user_id}
        ).mappings().all()

def get_skill_progress(user_id):
    with engine.connect() as conn:
        row = conn.execute(
            text("""
                SELECT
                    COUNT(*) AS total_skills,
                    SUM(CASE WHEN status = 'verified' THEN 1 ELSE 0 END) AS verified_skills
                FROM user_skills
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).mappings().first()

    total = row["total_skills"] or 0
    verified = row["verified_skills"] or 0

    percentage = int((verified / total) * 100) if total > 0 else 0

    return {
        "total": total,
        "verified": verified,
        "percentage": percentage
    }

def get_applied_jobs(user_id, status, search, offset, limit):
    base = """
        FROM job_applications ja
        JOIN job j ON j.id = ja.job_id
        WHERE ja.user_id = :uid
    """

    filters = {}
    if status:
        base += " AND ja.status = :status"
        filters["status"] = status

    if search:
        base += " AND j.title LIKE :search"
        filters["search"] = f"%{search}%"

    data_sql = f"""
        SELECT
            'job' AS type,
            j.title,
            ja.status,
            ja.applied_at
        {base}
        ORDER BY ja.applied_at DESC
        LIMIT :limit OFFSET :offset
    """

    count_sql = f"SELECT COUNT(*) {base}"

    with engine.connect() as conn:
        data = conn.execute(
            text(data_sql),
            dict(uid=user_id, limit=limit, offset=offset, **filters)
        ).mappings().all()

        count = conn.execute(
            text(count_sql),
            dict(uid=user_id, **filters)
        ).scalar()

    return data, count

def get_applied_assignments(user_id, status, search, offset, limit):
    base = """
        FROM assignment_applications aa
        JOIN assignments a ON a.id = aa.assignment_id
        WHERE aa.user_id = :uid
    """

    filters = {}
    if status:
        base += " AND aa.application_status = :status"
        filters["status"] = status

    if search:
        base += " AND a.title LIKE :search"
        filters["search"] = f"%{search}%"

    data_sql = f"""
        SELECT
            'assignment' AS type,
            a.title,
            aa.application_status AS status,
            aa.applied_at
        {base}
        ORDER BY aa.applied_at DESC
        LIMIT :limit OFFSET :offset
    """

    count_sql = f"SELECT COUNT(*) {base}"

    with engine.connect() as conn:
        data = conn.execute(
            text(data_sql),
            dict(uid=user_id, limit=limit, offset=offset, **filters)
        ).mappings().all()

        count = conn.execute(
            text(count_sql),
            dict(uid=user_id, **filters)
        ).scalar()

    return data, count

def get_user_courses_raw(user_id, search=None, offset=0, limit=6):
    sql = """
        SELECT DISTINCT c.id, c.title, c.created_at
        FROM courses c
        JOIN quizzes q ON q.course_id = c.id
        JOIN user_quiz_attempts uqa ON uqa.quiz_id = q.id
        WHERE uqa.user_id = :uid
          AND c.is_active = 1
    """

    params = {"uid": user_id}

    if search:
        sql += " AND c.title LIKE :search"
        params["search"] = f"%{search}%"

    sql += """
        ORDER BY c.created_at DESC
        LIMIT :limit OFFSET :offset
    """

    params["limit"] = limit
    params["offset"] = offset

    with engine.connect() as conn:
        return conn.execute(
            text(sql), params
        ).mappings().all()


def get_user_courses_count(user_id, search=None):
    sql = """
        SELECT COUNT(DISTINCT c.id)
        FROM courses c
        JOIN quizzes q ON q.course_id = c.id
        JOIN user_quiz_attempts uqa ON uqa.quiz_id = q.id
        WHERE uqa.user_id = :uid
          AND c.is_active = 1
    """

    params = {"uid": user_id}

    if search:
        sql += " AND c.title LIKE :search"
        params["search"] = f"%{search}%"

    with engine.connect() as conn:
        return conn.execute(
            text(sql), params
        ).scalar()


def get_skill_id(course_id):
    with engine.connect() as conn:
        return conn.execute(
            text("select skill_id from courses where id = :course_id"),
            {"course_id": course_id}
        ).mappings().first()