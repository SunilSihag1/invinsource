document.addEventListener("DOMContentLoaded", () => {

    gsap.from(".success-card", {
        opacity: 0,
        y: 30,
        duration: 0.8,
        ease: "power3.out"
    });

    gsap.from(".title, .subtitle, .desc", {
        opacity: 0,
        y: 20,
        duration: 0.6,
        stagger: 0.15,
        delay: 0.2
    });

    gsap.from(".subscription-box", {
        opacity: 0,
        y: 20,
        duration: 0.6,
        delay: 0.6
    });

    gsap.from(".check-circle", {
        scale: 0.6,
        opacity: 0,
        duration: 0.6,
        ease: "back.out(1.8)",
        delay: 0.8
    });

    gsap.to(".check-circle", {
        scale: 1.05,
        repeat: -1,
        yoyo: true,
        duration: 1.2,
        ease: "power1.inOut",
        delay: 1.6
    });

});
