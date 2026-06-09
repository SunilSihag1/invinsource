/* WELCOME */
lottie.loadAnimation({
    container: document.getElementById('welcomeAnim'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://assets5.lottiefiles.com/packages/lf20_touohxv0.json'
});

/* STATS */
lottie.loadAnimation({
    container: document.getElementById('earningAnim'),
    path: 'https://assets1.lottiefiles.com/packages/lf20_3vbOcw.json',
    loop: true,
    autoplay: true
});

lottie.loadAnimation({
    container: document.getElementById('jobAnim'),
    path: 'https://assets2.lottiefiles.com/packages/lf20_xlmz9xwm.json',
    loop: true,
    autoplay: true
});

lottie.loadAnimation({
    container: document.getElementById('assignAnim'),
    path: 'https://assets4.lottiefiles.com/packages/lf20_jtbfg2nb.json',
    loop: true,
    autoplay: true
});

/* COUNT UP */
document.querySelectorAll('[data-count]').forEach(el => {
    let target = +el.dataset.count;
    let current = 0;
    let step = target / 60;

    let interval = setInterval(() => {
        current += step;
        if (current >= target) {
            el.innerText = target;
            clearInterval(interval);
        } else {
            el.innerText = Math.floor(current);
        }
    }, 20);
});

document.querySelectorAll(".action-lottie").forEach(el => {
    lottie.loadAnimation({
        container: el,
        renderer: "svg",
        loop: true,
        autoplay: false,
        path: "https://assets7.lottiefiles.com/packages/lf20_w51pcehl.json"
    });

    el.parentElement.addEventListener("mouseenter", () => {
        el.firstChild?.play();
    });
});
    