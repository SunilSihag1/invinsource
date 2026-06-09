document.addEventListener("DOMContentLoaded", () => {

    // PAGE FADE IN
    gsap.from("body", {
        opacity: 0,
        duration: 0.4,
        ease: "power2.out"
    });

    // SECTION FADE + SLIDE
    gsap.from(".animate-section", {
        opacity: 0,
        y: 40,
        duration: 0.7,
        stagger: 0.15,
        ease: "power3.out"
    });

    // CARD STAGGER
    gsap.from(".animate-card", {
        opacity: 0,
        y: 30,
        duration: 0.6,
        stagger: 0.12,
        ease: "power3.out"
    });

});
