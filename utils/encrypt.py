from itsdangerous import URLSafeSerializer
import re
from config import FLASK_SECRET_KEY

serializer = URLSafeSerializer(
    secret_key=FLASK_SECRET_KEY,
    salt="job-id"
)
def encrypt_id(real_id):
    return serializer.dumps(real_id)
def decrypt_id(enc_id):
    try:
        return serializer.loads(enc_id)
    except Exception:
        return None

dashboard_serializer = URLSafeSerializer(
    secret_key=FLASK_SECRET_KEY,
    salt="dashboard-user"
)
def encrypt_user_id(user_id):
    return dashboard_serializer.dumps(user_id)
def decrypt_user_id(enc_uid):
    try:
        return dashboard_serializer.loads(enc_uid)
    except Exception:
        return None

lms_serializer = URLSafeSerializer(
    secret_key=FLASK_SECRET_KEY,
    salt="lms-id"
)

def encrypt_lms_id(real_id):
    return lms_serializer.dumps(int(real_id))

def decrypt_lms_id(enc_id):
    try:
        return int(lms_serializer.loads(enc_id))
    except Exception:
        return None
    
skill_serializer = URLSafeSerializer(
    secret_key=FLASK_SECRET_KEY,
    salt="skill-id"
)

def encrypt_skill_id(real_id):
    return skill_serializer.dumps(int(real_id))

def decrypt_skill_id(enc_id):
    try:
        return int(skill_serializer.loads(enc_id))
    except Exception:
        return None

subscription_serializer = URLSafeSerializer(
    secret_key=FLASK_SECRET_KEY,
    salt="subscription-id"
)

def encrypt_subscription_id(subscription_id):
    return subscription_serializer.dumps(int(subscription_id))


def decrypt_subscription_id(enc_subscription_id):
    try:
        return int(subscription_serializer.loads(enc_subscription_id))
    except Exception:
        return None


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
