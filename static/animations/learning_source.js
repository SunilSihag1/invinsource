/* ================= PAGE FADE ================= */
gsap.from(".lms-bg", {
    opacity: 0,
    duration: 0.4,
    ease: "power2.out"
});

/* ================= MANDATORY SECTION ================= */
gsap.from(".mandatory-section", {
    y: 20,
    opacity: 0,
    duration: 0.6,
    ease: "power3.out"
});

/* ================= MANDATORY CARD ================= */
gsap.from(".mandatory-card", {
    scale: 0.97,
    opacity: 0,
    duration: 0.5,
    delay: 0.15,
    ease: "power3.out"
});

/* ================= PROGRESS BAR ANIMATION ================= */
document.querySelectorAll(".progress-fill").forEach(bar => {
    const width = bar.style.width;
    bar.style.width = "0%";

    gsap.to(bar, {
        width: width,
        duration: 0.9,
        delay: 0.4,
        ease: "power3.out"
    });
});

/* ================= OPEN COURSES GRID ================= */
gsap.from(".open-section h2", {
    y: 15,
    opacity: 0,
    duration: 0.4,
    delay: 0.3,
    ease: "power2.out"
});

gsap.from(".open-card", {
    y: 18,
    opacity: 0,
    duration: 0.45,
    stagger: 0.08,
    delay: 0.45,
    ease: "power2.out"
});

document.addEventListener("DOMContentLoaded", () => {

    /* ===== PAGE FADE ===== */
    gsap.from(".lms-bg", {
        opacity: 0,
        duration: 0.4,
        ease: "power2.out"
    });

    /* ===== PROGRESS BAR RESET + ANIMATE ===== */
    document.querySelectorAll(".progress-fill").forEach(bar => {

        // actual width (from inline style)
        const targetWidth = bar.style.width;

        // ALWAYS RESET FIRST
        bar.style.width = "0%";

        // force browser repaint (IMPORTANT)
        bar.offsetHeight;

        // animate to actual %
        gsap.to(bar, {
            width: targetWidth,
            duration: 1,
            delay: 0.3,
            ease: "power3.out"
        });
    });

    /* ===== MANDATORY CARD ===== */
    gsap.from(".mandatory-card", {
        y: 20,
        opacity: 0,
        duration: 0.6,
        delay: 0.1,
        ease: "power3.out"
    });

    /* ===== OPEN COURSES ===== */
    gsap.from(".open-card", {
        y: 15,
        opacity: 0,
        duration: 0.45,
        stagger: 0.08,
        delay: 0.35,
        ease: "power2.out"
    });

});