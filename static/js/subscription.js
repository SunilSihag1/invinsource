let selectedPlanCode = null;

function buyPlan(plan) {
    selectedPlanCode = plan;

    fetch(`/subscription/${encUserId}/order`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            plan_code: plan
        })
    })
    .then(res => res.json())
    .then(data => {
        openRazorpay(data);
    });
}

function openRazorpay(order) {

    var options = {
        key: order.key,
        amount: order.amount,
        currency: "INR",
        name: "Invinsource",
        description: "Subscription Purchase",
        order_id: order.order_id,

        // ✅ SUCCESS
        handler: function (response) {
            fetch(`/subscription/${encUserId}/verify-payment`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_signature: response.razorpay_signature,
                    plan_code: selectedPlanCode
                })
            })
            .then(res => res.json())
            .then(data => {
                window.location.href = data.success
                    ? "/payment-status?status=success"
                    : "/payment-status?status=failed";
            });
        },

        modal: {
            // ❌ USER CANCELLED
            ondismiss: function () {
                notifyPaymentFailed();
            }
        }
    };

    var rzp = new Razorpay(options);

    // ❌ PAYMENT FAILED
    rzp.on('payment.failed', function (response) {
        notifyPaymentFailed(response);
    });

    rzp.open();
}

function notifyPaymentFailed(response = null) {

    fetch(`/subscription/${encUserId}/payment-failed`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            plan_code: selectedPlanCode,
            razorpay_payment_id: response?.error?.metadata?.payment_id || null,
            razorpay_order_id: response?.error?.metadata?.order_id || null,
            error_code: response.error.code || null,
            error_reason: response.error.description || null
        })
    })
    .finally(() => {
        window.location.href = "/payment-status?status=failed";
    });
}
