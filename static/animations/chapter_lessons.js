function markWatched(lessonId, btn) {
    btn.disabled = true;
    btn.innerText = "Marking...";

    fetch(`/lesson/${lessonId}/watched`, {
        method: "POST"
    }).then(() => {
        const card = btn.closest(".lesson-card");

        gsap.to(card, {
            scale: 1.05,
            backgroundColor: "#ecfeff",
            duration: 0.25,
            yoyo: true,
            repeat: 1,
            ease: "power2.out",
            onComplete: () => {
                setTimeout(() => location.reload(), 300);
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       TITLE (NO REVERSE)
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

    /* ===============================
       LESSON CARDS (SAFE LOAD)
    =============================== */
    gsap.fromTo(".lesson-card:not(.done)",
        { y: 30, opacity: 0 },
        {
            y: 0,
            opacity: 1,
            duration: 0.6,
            stagger: 0.12,
            ease: "power3.out"
        }
    );

    /* ===============================
       COMPLETED LESSONS
    =============================== */
    gsap.fromTo(".lesson-card.done",
        { scale: 0.95, opacity: 0 },
        {
            scale: 1,
            opacity: 1,
            duration: 0.4,
            stagger: 0.08,
            ease: "back.out(1.7)",
            delay: 0.2
        }
    );

    /* ===============================
       CHAPTER COMPLETE BOX
    =============================== */
    const completeBox = document.querySelector(".animate-complete");
    if (completeBox) {
        gsap.fromTo(completeBox,
            { scale: 0.9, opacity: 0 },
            {
                scale: 1,
                opacity: 1,
                duration: 0.6,
                ease: "back.out(1.6)",
                delay: 0.3
            }
        );
    }

    /* ===============================
       QUIZ BUTTON PULSE
    =============================== */
    const pulseBtn = document.querySelector(".pulse");
    if (pulseBtn) {
        gsap.to(pulseBtn, {
            scale: 1.06,
            repeat: -1,
            yoyo: true,
            duration: 0.8,
            ease: "power1.inOut",
            delay: 1
        });
    }

});
