document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       TITLE + SUBTITLE
    =============================== */
    gsap.fromTo(".animate-title",
        { y: 20, opacity: 0 },
        {
            y: 0,
            opacity: 1,
            duration: 0.6,
            ease: "power2.out"
        }
    );

    gsap.fromTo(".animate-subtitle",
        { y: 10, opacity: 0 },
        {
            y: 0,
            opacity: 1,
            duration: 0.5,
            delay: 0.15,
            ease: "power2.out"
        }
    );

    /* ===============================
       QUESTIONS STAGGER
    =============================== */
    gsap.fromTo(".animate-question",
        { y: 30, opacity: 0 },
        {
            y: 0,
            opacity: 1,
            duration: 0.6,
            stagger: 0.15,
            ease: "power3.out",
            delay: 0.2
        }
    );

    /* ===============================
       SUBMIT BUTTON POP
    =============================== */
    gsap.fromTo(".animate-submit",
        { scale: 0.9, opacity: 0 },
        {
            scale: 1,
            opacity: 1,
            duration: 0.5,
            ease: "back.out(1.6)",
            delay: 0.5
        }
    );

    /* ===============================
       OPTION CLICK FEEDBACK
    =============================== */
    document.querySelectorAll(".option input").forEach(input => {
        input.addEventListener("change", () => {
            gsap.fromTo(input.closest("label"),
                { scale: 0.97 },
                {
                    scale: 1,
                    duration: 0.2,
                    ease: "power2.out"
                }
            );
        });
    });

});
