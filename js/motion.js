/**
 * Continental Detailing — Motion Design Engine
 * Headline word reveals, image curtains, scroll reveals, hero parallax,
 * navbar auto-hide, counters.
 */

(function () {
    'use strict';

    const root = document.documentElement;
    root.classList.add('js');
    window.__motionReady = true;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // =========================================
    // 1. HEADLINE SPLIT — each word rises from behind a mask
    // =========================================
    function splitWords(el) {
        if (el.dataset.splitDone) return;
        el.dataset.splitDone = '1';
        el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());

        const baseDelay = parseFloat(el.dataset.splitDelay || '0');
        let index = 0;

        (function walk(node) {
            Array.from(node.childNodes).forEach((child) => {
                if (child.nodeType === Node.TEXT_NODE) {
                    const frag = document.createDocumentFragment();
                    child.textContent.split(/(\s+)/).forEach((part) => {
                        if (!part) return;
                        if (/^\s+$/.test(part)) {
                            frag.appendChild(document.createTextNode(' '));
                            return;
                        }
                        const outer = document.createElement('span');
                        outer.className = 'sw';
                        outer.setAttribute('aria-hidden', 'true');
                        const inner = document.createElement('span');
                        inner.className = 'sw-i';
                        inner.textContent = part;
                        inner.style.transitionDelay = (baseDelay + index * 0.07).toFixed(2) + 's';
                        index++;
                        outer.appendChild(inner);
                        frag.appendChild(outer);
                    });
                    node.replaceChild(frag, child);
                } else if (child.nodeType === Node.ELEMENT_NODE && child.tagName !== 'BR') {
                    walk(child);
                }
            });
        })(el);
    }

    if (!reducedMotion) {
        document.querySelectorAll('[data-split]').forEach(splitWords);
    }

    // =========================================
    // 2. SCROLL REVEAL — Intersection Observer
    // =========================================
    const revealSelector = '.reveal, .reveal-left, .reveal-right, .reveal-scale, .line-grow, [data-split], .img-reveal';
    const revealElements = document.querySelectorAll(revealSelector);

    function markRevealed(el) {
        el.classList.add('revealed');
        // After the entrance finishes, drop stagger delays so hover feedback is instant
        setTimeout(() => el.classList.add('reveal-done'), 2200);
    }

    if ('IntersectionObserver' in window && !reducedMotion) {
        // An .img-reveal starts fully clipped, and Chromium treats a fully clipped
        // element as never intersecting — so we watch its parent instead.
        const watched = new Map();

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    (watched.get(entry.target) || []).forEach(markRevealed);
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12,
            rootMargin: '0px 0px -8% 0px'
        });

        revealElements.forEach((el) => {
            const target = el.classList.contains('img-reveal') && el.parentElement ? el.parentElement : el;
            if (!watched.has(target)) watched.set(target, []);
            watched.get(target).push(el);
            revealObserver.observe(target);
        });
    } else {
        revealElements.forEach(markRevealed);
    }

    // =========================================
    // 3. PARALLAX — Hero background
    // =========================================
    const parallaxBg = document.querySelector('.parallax-bg');

    if (parallaxBg && !reducedMotion) {
        let ticking = false;

        function updateParallax() {
            const y = window.scrollY;
            if (y < window.innerHeight * 1.2) {
                parallaxBg.style.transform = `translate3d(0, ${y * 0.25}px, 0) scale(1.08)`;
            }
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });

        parallaxBg.style.transform = 'translate3d(0, 0, 0) scale(1.08)';
    }

    // =========================================
    // 4. NAVBAR — Auto-hide on scroll down
    // =========================================
    const nav = document.querySelector('nav');

    if (nav) {
        let lastScrollY = 0;
        let navTicking = false;

        function updateNav() {
            const currentScrollY = window.scrollY;

            if (currentScrollY > 100) {
                if (currentScrollY > lastScrollY && currentScrollY > 200) {
                    nav.classList.add('nav-hidden');
                    nav.classList.remove('nav-visible');
                } else {
                    nav.classList.remove('nav-hidden');
                    nav.classList.add('nav-visible');
                    nav.style.backgroundColor = 'rgba(255, 255, 255, 0.96)';
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
    // 5. COUNTER ANIMATION — Animate numbers
    // =========================================
    const counters = document.querySelectorAll('[data-count]');

    function animateCounter(el) {
        const target = parseFloat(el.dataset.count);
        const decimals = parseInt(el.dataset.decimals || '0', 10);
        const suffix = el.dataset.suffix || '';

        if (reducedMotion) {
            el.textContent = target.toFixed(decimals) + suffix;
            return;
        }

        const duration = 1800;
        const startTime = performance.now();

        function step(currentTime) {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 4);
            el.textContent = (eased * target).toFixed(decimals) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach((el) => counterObserver.observe(el));
    } else {
        counters.forEach(animateCounter);
    }

    // ─── Lazy videos ───
    // <video data-src> is only downloaded once it nears the screen, then plays
    // while visible and pauses off-screen. Reduced motion: first frame/poster only.
    const lazyVideos = document.querySelectorAll('video[data-src]');
    function loadVideo(video) {
        if (!video.getAttribute('src')) video.src = video.getAttribute('data-src');
    }
    if (lazyVideos.length && 'IntersectionObserver' in window) {
        const videoObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                const video = entry.target;
                if (entry.isIntersecting) {
                    loadVideo(video);
                    if (reducedMotion) return;
                    const p = video.play();
                    if (p && p.catch) p.catch(() => { /* autoplay refused: poster stays */ });
                } else if (video.getAttribute('src')) {
                    video.pause();
                }
            });
        }, { rootMargin: '200px 0px', threshold: 0.01 });
        lazyVideos.forEach((v) => videoObserver.observe(v));
    } else {
        lazyVideos.forEach(loadVideo);
    }

    // =========================================
    // 6. SCROLL PROGRESS — thin bar at the top of the page
    // =========================================
    if (!reducedMotion) {
        const bar = document.createElement('div');
        bar.className = 'scroll-progress';
        bar.setAttribute('aria-hidden', 'true');
        document.body.appendChild(bar);
        let pTick = false;
        const paint = () => {
            const max = document.documentElement.scrollHeight - window.innerHeight;
            bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ')';
            pTick = false;
        };
        window.addEventListener('scroll', () => {
            if (!pTick) { requestAnimationFrame(paint); pTick = true; }
        }, { passive: true });
        paint();
    }

    // =========================================
    // 7. ACTION BAR — price + WhatsApp always one thumb away on mobile.
    // Skipped on pages that already carry their own bottom bar or a payment step.
    // =========================================
    const page = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    const noBar = ['services.html', 'services', 'acompte.html', 'reglement.html', 'acompte', 'reglement'];
    if (noBar.indexOf(page) === -1 && !document.querySelector('.action-bar')) {
        const ab = document.createElement('div');
        ab.className = 'action-bar';
        ab.innerHTML =
            '<a class="action-bar__price" href="/services.html" data-track="barre_prix">Mon prix <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>' +
            '<a class="action-bar__wa" href="https://wa.me/33750875964?text=' +
            encodeURIComponent('Bonjour, je souhaite un renseignement pour le nettoyage de ma voiture 🚗') +
            '" target="_blank" rel="noopener noreferrer" data-track="barre_whatsapp"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> WhatsApp</a>';
        document.body.appendChild(ab);

        ab.addEventListener('click', (e) => {
            const a = e.target.closest('a[data-track]');
            if (!a) return;
            if (window.gtag) window.gtag('event', a.dataset.track);
            if (window.va) window.va('event', { name: a.dataset.track });
        });

        const footer = document.querySelector('footer');
        let abTick = false;
        const place = () => {
            const cookie = document.querySelector('.cookie-banner:not([hidden])');
            const menuOpen = document.body.style.overflow === 'hidden';
            const nearFooter = footer && footer.getBoundingClientRect().top < window.innerHeight - 40;
            const on = window.scrollY > window.innerHeight * 0.6 && !cookie && !menuOpen && !nearFooter;
            ab.classList.toggle('is-on', on);
            abTick = false;
        };
        window.addEventListener('scroll', () => {
            if (!abTick) { requestAnimationFrame(place); abTick = true; }
        }, { passive: true });
        document.addEventListener('click', () => setTimeout(place, 50));
        place();
    }

    // =========================================
    // 8. RAILS — on phones, cards scroll sideways; dots show the position
    // =========================================
    if (window.matchMedia('(max-width: 767px)').matches) {
        document.querySelectorAll('.m-rail').forEach((rail) => {
            const cards = Array.from(rail.children);
            if (cards.length < 2) return;
            const dots = document.createElement('div');
            dots.className = 'rail-dots';
            dots.setAttribute('aria-hidden', 'true');
            cards.forEach(() => dots.appendChild(document.createElement('i')));
            rail.insertAdjacentElement('afterend', dots);
            let t = false;
            const sync = () => {
                const mid = rail.scrollLeft + rail.clientWidth / 2;
                let best = 0, dist = Infinity;
                cards.forEach((c, k) => {
                    const d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid);
                    if (d < dist) { dist = d; best = k; }
                });
                Array.from(dots.children).forEach((d, k) => d.classList.toggle('on', k === best));
                t = false;
            };
            rail.addEventListener('scroll', () => { if (!t) { requestAnimationFrame(sync); t = true; } }, { passive: true });
            sync();
        });
    }

})();
