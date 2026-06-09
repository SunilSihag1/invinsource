document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       PAGE FADE IN
    =============================== */
    gsap.fromTo(".animate-wrapper",
        { opacity: 0 },
        {
            opacity: 1,
            duration: 0.4,
            ease: "power1.out"
        }
    );

    /* ===============================
       SCORE POP
    =============================== */
    gsap.fromTo(".animate-score",
        { scale: 0.8, opacity: 0 },
        {
            scale: 1,
            opacity: 1,
            duration: 0.6,
            ease: "back.out(1.7)"
        }
    );

    /* ===============================
       PASS / FAIL MESSAGE
    =============================== */
    gsap.fromTo(".animate-status",
        { y: 15, opacity: 0 },
        {
            y: 0,
            opacity: 1,
            duration: 0.5,
            delay: 0.2,
            ease: "power2.out"
        }
    );

    /* ===============================
       CTA BUTTON POP
    =============================== */
    gsap.fromTo(".animate-cta",
        { scale: 0.9, opacity: 0 },
        {
            scale: 1,
            opacity: 1,
            duration: 0.4,
            delay: 0.4,
            ease: "back.out(1.6)"
        }
    );

    /* ===============================
       PASS → PULSE CTA
    =============================== */
    const pulseBtn = document.querySelector(".pulse");
    if (pulseBtn) {
        gsap.to(pulseBtn, {
            scale: 1.05,
            repeat: -1,
            yoyo: true,
            duration: 0.8,
            ease: "power1.inOut",
            delay: 1
        });
    }

    /* ===============================
       FAIL → SHAKE CTA
    =============================== */
    const shakeBtn = document.querySelector(".shake");
    if (shakeBtn) {
        gsap.fromTo(shakeBtn,
            { x: -6 },
            {
                x: 6,
                repeat: 4,
                yoyo: true,
                duration: 0.08,
                ease: "power1.inOut",
                delay: 0.6
            }
        );
    }

});
