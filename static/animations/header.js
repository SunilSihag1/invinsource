/* ================= NAVBAR LOAD ================= */
gsap.from(".navbar", {
    y: -80,
    opacity: 0,
    duration: 0.8,
    ease: "power3.out"
});

gsap.from(".logo", {
    opacity: 0,
    scale: 0.95,
    duration: 0.6,
    delay: 0.2,
    ease: "power3.out"
});

gsap.from(".navbar nav a", {
    opacity: 0,
    y: -10,
    duration: 0.5,
    stagger: 0.1,
    delay: 0.4,
    ease: "power3.out"
});

/* ================= STICKY SHADOW ================= */
window.addEventListener("scroll", () => {
    const nav = document.querySelector(".navbar");
    if (window.scrollY > 20) {
        nav.classList.add("scrolled");
    } else {
        nav.classList.remove("scrolled");
    }
});
