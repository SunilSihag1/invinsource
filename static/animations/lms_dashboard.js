document.addEventListener("DOMContentLoaded", () => {

    /* ================= PAGE ENTRY ================= */
    gsap.from(".lms-wrapper", {
        opacity: 0,
        y: 24,
        duration: 0.7,
        ease: "power3.out"
    });

    /* ================= SKILL CARD ================= */
    gsap.from(".skill-card", {
        opacity: 0,
        y: -16,
        duration: 0.5,
        delay: 0.1,
        ease: "power2.out"
    });

    /* ================= PROGRESS BAR (0 → %) ================= */
    const progressFill = document.querySelector(".progress-fill");
    if (progressFill) {
        const targetWidth = progressFill.style.width;
        progressFill.style.width = "0%";

        gsap.to(progressFill, {
            width: targetWidth,
            duration: 1.3,
            delay: 0.3,
            ease: "power3.out"
        });
    }

    /* ================= COURSE CARD ================= */
    gsap.from(".course-card", {
        opacity: 0,
        y: 14,
        duration: 0.45,
        delay: 0.25,
        ease: "power2.out"
    });

    /* ================= CHAPTERS STAGGER ================= */
    gsap.from(".chapter-card", {
        opacity: 0,
        y: 18,
        duration: 0.5,
        stagger: 0.08,
        delay: 0.35,
        ease: "power2.out"
    });

    /* ================= LOCKED CHAPTER FEEL ================= */
    gsap.utils.toArray(".chapter-card.locked").forEach(card => {
        gsap.to(card, {
            opacity: 0.55,
            duration: 0.3
        });
    });

    /* ================= FINAL QUIZ CARD ================= */
    gsap.from(".final-quiz-card", {
        opacity: 0,
        scale: 0.96,
        duration: 0.55,
        delay: 0.55,
        ease: "power3.out"
    });

});
