/* ================= PAGE FADE ================= */
gsap.from(".apply-wrapper", {
    opacity: 0,
    duration: 0.4,
    ease: "power2.out"
});

/* ================= CARD ENTRANCE ================= */
gsap.from(".apply-card", {
    y: 36,
    scale: 0.97,
    opacity: 0,
    duration: 0.7,
    ease: "power3.out"
});

/* ================= TITLE + SUBTITLE ================= */
gsap.from(".apply-form h2, .apply-form .subtext", {
    y: 14,
    opacity: 0,
    duration: 0.45,
    stagger: 0.12,
    delay: 0.25,
    ease: "power2.out"
});

/* ================= FORM FIELDS ================= */
gsap.from(
    ".apply-form label, .apply-form input, .apply-form textarea",
    {
        y: 10,
        opacity: 0,
        duration: 0.35,
        stagger: 0.045,
        delay: 0.45,
        ease: "power1.out"
    }
);

/* ================= BUTTON ROW ================= */
gsap.from(".btn-row", {
    y: 12,
    opacity: 0,
    duration: 0.4,
    delay: 0.9,
    ease: "power2.out"
});

/* ================= FLASH MESSAGE SHAKE ================= */
const flashError = document.querySelector(".flash-error");
if (flashError) {
    gsap.fromTo(
        flashError,
        { x: -6 },
        {
            x: 6,
            duration: 0.08,
            repeat: 5,
            yoyo: true,
            ease: "power1.inOut"
        }
    );
}

/* ================= SUBMIT LOADING ================= */
const form = document.querySelector("form");
const submitBtn = document.querySelector(".btn-primary");

if (form && submitBtn) {
    form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.innerText = "Submitting...";
        submitBtn.style.opacity = "0.85";
    });
}