/* ================= PAGE FADE IN ================= */
gsap.from(".apply-wrapper", {
    opacity: 0,
    duration: 0.4,
    ease: "power2.out"
});

/* ================= APPLY CARD ================= */
gsap.from(".apply-card", {
    y: 40,
    scale: 0.96,
    opacity: 0,
    duration: 0.8,
    ease: "power3.out"
});

/* ================= FORM CONTENT ================= */
gsap.from(".apply-form > h2, .apply-form > .subtext", {
    y: 12,
    opacity: 0,
    duration: 0.5,
    stagger: 0.1,
    delay: 0.3,
    ease: "power2.out"
});

/* ================= FORM FIELDS ================= */
gsap.from(".apply-form label, .apply-form input, .apply-form textarea, .file-input", {
    y: 10,
    opacity: 0,
    duration: 0.4,
    stagger: 0.04,
    delay: 0.45,
    ease: "power1.out"
});

/* ================= BUTTON ROW ================= */
gsap.from(".btn-row", {
    y: 12,
    opacity: 0,
    duration: 0.4,
    delay: 0.9,
    ease: "power2.out"
});

/* ================= ERROR SHAKE ================= */
const errorFlash = document.querySelector(".flash-error");
if (errorFlash) {
    gsap.fromTo(errorFlash,
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
        submitBtn.style.opacity = "0.8";
    });
}