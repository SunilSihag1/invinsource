/* ================= PAGE LOAD ================= */
gsap.from(".page", {
    opacity: 0,
    duration: 0.6,
    ease: "power2.out"
});

/* ================= CARD ================= */
gsap.from(".login-card", {
    y: 40,
    scale: 0.96,
    opacity: 0,
    duration: 0.8,
    ease: "power3.out"
});

/* ================= LEFT ILLUSTRATION ================= */
gsap.from(".login-illustration", {
    x: -60,
    opacity: 0,
    duration: 0.8,
    delay: 0.2,
    ease: "power3.out"
});

/* ================= FORM CONTENT ================= */
gsap.from(".login-form > *", {
    y: 16,
    opacity: 0,
    duration: 0.6,
    stagger: 0.08,
    delay: 0.4,
    ease: "power3.out"
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