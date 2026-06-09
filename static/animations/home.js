
gsap.registerPlugin(ScrollTrigger);

/* ================= HERO ================= */
gsap.from(".hero-text h1", {
    y: 40,
    opacity: 0,
    duration: 1,
    ease: "power3.out"
});

gsap.from(".hero-text p", {
    y: 30,
    opacity: 0,
    duration: 0.8,
    delay: 0.3,
    ease: "power3.out"
});

gsap.from(".hero-actions a", {
    y: 20,
    opacity: 0,
    duration: 0.6,
    delay: 0.5,
    stagger: 0.15,
    ease: "power3.out"
});

/* ================= HERO MOCK CARD ================= */
gsap.to(".mock-card", {
    y: -12,
    repeat: -1,
    yoyo: true,
    duration: 2,
    ease: "sine.inOut"
});

/* ================= HOW IT WORKS ================= */
gsap.from(".step-card", {
    scrollTrigger: {
        trigger: ".steps",
        start: "top 80%",
    },
    y: 40,
    opacity: 0,
    duration: 0.7,
    stagger: 0.2,
    ease: "power3.out"
});

/* ================= FEATURES ================= */
gsap.from(".feature-card", {
    scrollTrigger: {
        trigger: ".features",
        start: "top 80%",
    },
    y: 40,
    opacity: 0,
    duration: 0.7,
    stagger: 0.15,
    ease: "power3.out"
});
