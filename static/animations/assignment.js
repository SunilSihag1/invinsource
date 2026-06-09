/* ================= PAGE LOAD ================= */
gsap.from(".wrapper", {
    opacity: 0,
    duration: 0.35,
    ease: "power2.out"
});

/* ================= LEFT LIST ================= */
gsap.from(".job-list", {
    x: -40,
    opacity: 0,
    duration: 0.6,
    ease: "power3.out"
});

/* ================= ASSIGNMENT ITEMS ================= */
gsap.from(".job-item", {
    y: 10,
    opacity: 0,
    duration: 0.35,
    stagger: 0.05,
    delay: 0.2,
    ease: "power1.out"
});

/* ================= RIGHT DETAILS ================= */
gsap.from(".job-details", {
    x: 40,
    opacity: 0,
    duration: 0.6,
    delay: 0.15,
    ease: "power3.out"
});

/* ================= DETAILS CONTENT ================= */
gsap.from(
    ".job-header h2, .job-header .location, .description, .info-grid > div",
    {
        y: 12,
        opacity: 0,
        duration: 0.4,
        stagger: 0.08,
        delay: 0.35,
        ease: "power2.out"
    }
);

/* ================= LISTS ================= */
gsap.from(".responsibilities li, .skills span", {
    y: 6,
    opacity: 0,
    duration: 0.3,
    stagger: 0.04,
    delay: 0.55,
    ease: "power1.out"
});

/* ================= APPLY BUTTON ================= */
gsap.from(".apply-btn", {
    scale: 0.96,
    opacity: 0,
    duration: 0.35,
    delay: 0.75,
    ease: "power2.out"
});

/* ================= ACTIVE ITEM HIGHLIGHT ================= */
const activeItem = document.querySelector(".job-item.active");
if (activeItem) {
    gsap.fromTo(
        activeItem,
        { scale: 0.98 },
        {
            scale: 1,
            duration: 0.35,
            ease: "elastic.out(1, 0.6)"
        }
    );
}