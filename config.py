import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
TEST_RAZORPAY_KEY_ID = os.getenv("TEST_RAZORPAY_KEY_ID")
TEST_RAZORPAY_KEY_SECRET = os.getenv("TEST_RAZORPAY_KEY_SECRET")


UPLOAD_FOLDER = "static/uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
