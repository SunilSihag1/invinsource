import razorpay
from flask import Blueprint, request, jsonify
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, TEST_RAZORPAY_KEY_ID, TEST_RAZORPAY_KEY_SECRET
from flask import render_template, session, abort
from database import get_subscriptions_from_db, get_subscription_by_plan_code, insert_payment, insert_user_subscription, get_latest_success_payment, get_latest_failed_payment, get_plan_code_from_plan_name, get_active_subscription
from utils.encrypt import decrypt_user_id, encrypt_user_id
from jobs.routes import login_required
from datetime import date, timedelta


payment_bp = Blueprint("payment", __name__)

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))     
test_client = razorpay.Client(auth=(TEST_RAZORPAY_KEY_ID, TEST_RAZORPAY_KEY_SECRET))

@payment_bp.route("/subscription/<enc_userid>")
@login_required
def sub(enc_userid):

    user_id = decrypt_user_id(enc_userid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)
    
    sub_details = get_active_subscription(user_id)

    subscriptions = get_subscriptions_from_db()
    return render_template(
        "subscription.html",
        subscriptions=subscriptions,
        sub_details = sub_details,
        user_id=user_id,
        enc_userid = enc_userid
    )


@payment_bp.route("/subscription/<enc_userid>/order", methods=["POST"])
@login_required
def create_order(enc_userid):

    data = request.get_json()
    if not data or "plan_code" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_id = decrypt_user_id(enc_userid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    data = request.get_json()
    plan_code = data["plan_code"]
    if not data or "plan_code" not in data:
        return jsonify({"error": "Invalid request"}), 400


    plan = get_subscription_by_plan_code(plan_code)
    if not plan:
        return jsonify({"error": "Invalid plan"}), 400

    amount = plan["price"] * 100

    order = test_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        "order_id": order["id"],
        "amount": order["amount"],
        "key": TEST_RAZORPAY_KEY_ID
    })

@payment_bp.route("/subscription/<enc_userid>/verify-payment", methods=["POST"])
@login_required
def verify_payment(enc_userid):

    user_id = decrypt_user_id(enc_userid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    data = request.get_json()
    required = [
        "razorpay_payment_id",
        "razorpay_order_id",
        "razorpay_signature",
        "plan_code"
    ]

    if not data or not all(k in data for k in required):
        return jsonify({"success": False}), 400

    plan_code = data["plan_code"]
    plan = get_subscription_by_plan_code(plan_code)

    if not plan:
        return jsonify({"success": False}), 400

    try:
        # ✅ VERIFY SIGNATURE (SUCCESS PATH)
        test_client.utility.verify_payment_signature({
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        start_date = date.today()
        end_date = start_date + timedelta(days=plan["duration_days"])

        # ✅ SUBSCRIPTION INSERT (ONLY ON SUCCESS)
        insert_user_subscription(
            user_id=user_id,
            subscription_id=plan["id"],
            start_date=start_date,
            end_date=end_date,
            amount_paid=plan["price"],
            payment_status="paid",
            subscription_status="active",
            razorpay_payment_id=data["razorpay_payment_id"],
            razorpay_order_id=data["razorpay_order_id"]
        )

        # ✅ PAYMENT INSERT (SUCCESS)
        insert_payment(
            user_id=user_id,
            amount=plan["price"],
            razorpay_payment_id=data["razorpay_payment_id"],
            razorpay_order_id=data["razorpay_order_id"],
            razorpay_signature=data["razorpay_signature"],
            status="success",
            error_code=None,
            error_reason=None
        )

        return jsonify({"success": True})

    except Exception as e:
        # ❌ PAYMENT FAILED / CANCELLED / INVALID SIGNATURE
        print("PAYMENT FAILED:", e)

        # ✅ PAYMENT INSERT (FAILED)
        insert_payment(
            user_id=user_id,
            amount=plan["price"],
            razorpay_payment_id=data.get("razorpay_payment_id"),
            razorpay_order_id=data.get("razorpay_order_id"),
            razorpay_signature=data.get("razorpay_signature"),
            status="failed",
            error_code=data.get("error_code"),
            error_reason=data.get("error_reason")
        )

        return jsonify({"success": False})


@payment_bp.route("/subscription/<enc_userid>/payment-failed", methods=["POST"])
@login_required
def payment_failed_backend(enc_userid):

    user_id = decrypt_user_id(enc_userid)
    if not user_id or user_id != session.get("user_id"):
        abort(403)

    data = request.get_json() or {}
    plan_code = data.get("plan_code")

    plan = get_subscription_by_plan_code(plan_code)
    if not plan:
        return jsonify({"success": False}), 400

    insert_payment(
        user_id=user_id,
        amount=plan["price"],
        razorpay_payment_id=data.get("razorpay_payment_id"),
        razorpay_order_id=data.get("razorpay_order_id"),
        razorpay_signature=None,
        status="failed",
        error_code=data.get("error_code"),
        error_reason=data.get("error_reason")
    )

    return jsonify({"success": True})



@payment_bp.route("/payment-status")
@login_required
def payment_status():

    user_id = session.get("user_id")
    status = request.args.get("status")

    # enc_user_id = encrypt_user_id(user_id)

    if status == "success":
        data = get_latest_success_payment(user_id)
        plan_code = get_plan_code_from_plan_name(data["plan_name"])

        if not data:
            abort(404)

        return render_template(
            "payment_status.html",
            status="success",
            plan_name=data["plan_name"],
            plan_code=plan_code,
            amount=f"₹{data['amount']}",
            payment_id=data["razorpay_payment_id"],
            billing_date=data["start_date"].strftime("%d %b %Y"),
            next_renewal=data["end_date"].strftime("%d %b %Y"),
            enc_userid=encrypt_user_id(user_id),
            
        )

    else:
        print(get_latest_failed_payment(user_id))
        data = get_latest_failed_payment(user_id)
        plan_code = get_plan_code_from_plan_name(data["plan_name"])

        if not data:
            abort(404)

        return render_template(
            "payment_status.html",
            status="failed",
            plan_name=data["plan_name"],
            plan_code=plan_code,
            amount=f"₹{data['amount']}",
            error_code=data["error_code"],
            error_reason=data["error_reason"],
            enc_userid=encrypt_user_id(user_id),
        )
