/* ================= PAGE FADE ================= */
gsap.from(".page", {
    opacity: 0,
    duration: 0.5,
    ease: "power2.out"
});

/* ================= CARD ================= */
gsap.from(".signup-card", {
    y: 40,
    scale: 0.96,
    opacity: 0,
    duration: 0.8,
    ease: "power3.out"
});

/* ================= ILLUSTRATION ================= */
gsap.from(".illustration", {
    x: -60,
    opacity: 0,
    duration: 0.8,
    delay: 0.2,
    ease: "power3.out"
});

/* ================= FORM CONTENT ================= */
gsap.from(".form-wrapper > *", {
    y: 16,
    opacity: 0,
    duration: 0.6,
    stagger: 0.08,
    delay: 0.35,
    ease: "power3.out"
});

/* ================= INPUT ROWS ================= */
gsap.from(".row input", {
    y: 12,
    opacity: 0,
    duration: 0.5,
    stagger: 0.06,
    delay: 0.5,
    ease: "power2.out"
});

/* ================= DOMAIN PILLS ================= */
gsap.from(".pill", {
    scale: 0.85,
    opacity: 0,
    duration: 0.4,
    stagger: 0.08,
    delay: 0.8,
    ease: "back.out(1.7)"
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