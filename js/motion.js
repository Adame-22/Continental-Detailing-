/**
 * Continental Detailing — Motion Design Engine
 * Scroll reveals, parallax, navbar auto-hide, counters
 */

(function () {
    'use strict';

    // =========================================
    // 1. SCROLL REVEAL — Intersection Observer
    // =========================================
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .line-grow');

    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target); // Animate once
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback: show everything immediately
        revealElements.forEach(el => el.classList.add('revealed'));
    }

    // =========================================
    // 2. PARALLAX — Hero background
    // =========================================
    const parallaxBg = document.querySelector('.parallax-bg');
    
    if (parallaxBg) {
        let ticking = false;

        function updateParallax() {
            const scrollY = window.scrollY;
            const speed = 0.3;
            parallaxBg.style.transform = `translateY(${scrollY * speed}px) scale(1.1)`;
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });

        // Initial scale to prevent gap
        parallaxBg.style.transform = 'translateY(0) scale(1.1)';
    }

    // =========================================
    // 3. NAVBAR — Auto-hide on scroll down
    // =========================================
    const nav = document.querySelector('nav');
    
    if (nav) {
        let lastScrollY = 0;
        let navTicking = false;

        function updateNav() {
            const currentScrollY = window.scrollY;

            if (currentScrollY > 100) {
                if (currentScrollY > lastScrollY && currentScrollY > 200) {
                    // Scrolling down & past threshold
                    nav.classList.add('nav-hidden');
                    nav.classList.remove('nav-visible');
                } else {
                    // Scrolling up
                    nav.classList.remove('nav-hidden');
                    nav.classList.add('nav-visible');
                    nav.style.backgroundColor = 'rgba(15, 23, 42, 0.95)';
                }
            } else {
                nav.classList.remove('nav-hidden');
                nav.style.backgroundColor = '';
            }

            lastScrollY = currentScrollY;
            navTicking = false;
        }

        window.addEventListener('scroll', () => {
            if (!navTicking) {
                requestAnimationFrame(updateNav);
                navTicking = true;
            }
        }, { passive: true });
    }

    // =========================================
    // 4. COUNTER ANIMATION — Animate numbers
    // =========================================
    const counters = document.querySelectorAll('[data-count]');

    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(el => counterObserver.observe(el));
    }

    function animateCounter(el) {
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 2000;
        const startTime = performance.now();

        function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(eased * target);
            el.textContent = current + suffix;

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }

        requestAnimationFrame(step);
    }

    // =========================================
    // 5. MAGNETIC CURSOR — CTA buttons
    // =========================================
    const magneticButtons = document.querySelectorAll('.glow-pulse');

    magneticButtons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.02)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });

    // =========================================
    // 6. TILT EFFECT — Cards
    // =========================================
    const tiltCards = document.querySelectorAll('.card-hover-lift');

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `translateY(-8px) perspective(800px) rotateX(${y * -5}deg) rotateY(${x * 5}deg)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });

})();
