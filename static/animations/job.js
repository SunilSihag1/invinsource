/* ================= PAGE LOAD ================= */
gsap.from(".job-list", {
    x: -40,
    opacity: 0,
    duration: 0.6,
    ease: "power3.out"
});

gsap.from(".job-item", {
    y: 14,
    opacity: 0,
    duration: 0.4,
    stagger: 0.05,
    delay: 0.2,
    ease: "power2.out"
});

gsap.from(".job-details", {
    y: 24,
    opacity: 0,
    duration: 0.6,
    delay: 0.4,
    ease: "power3.out"
});

/* ================= SKILL CHIPS ================= */
gsap.from(".job-details .skills span", {
    scale: 0.8,
    opacity: 0,
    duration: 0.3,
    stagger: 0.04,
    delay: 0.6,
    ease: "back.out(1.6)"
});

document.querySelectorAll(".job-item").forEach(item => {
    item.addEventListener("click", () => {
        gsap.to(".job-details", {
            opacity: 0,
            y: 10,
            duration: 0.15,
            ease: "power1.in"
        });
    });
});
