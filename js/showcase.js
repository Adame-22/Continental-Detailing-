/**
 * Continental Detailing — Showcase Engine v3
 * Layout: vehicle nav tabs (top) | car stage (left) | services panel (right)
 */
(function () {
    'use strict';

    const stdExt = [
        'Prélavage actif (Snow Foam)',
        'Nettoyage approfondi jantes & passages de roues',
        'Lavage manuel technique des 2 seaux',
        'Décontamination carrosserie',
        'Séchage premium & dressing des pneumatiques'
    ];

    const stdInt = [
        'Aspiration minutieuse (habitacle & coffre)',
        'Dégraissage des plastiques au pinceau',
        'Shampoing moquettes & tapis (Pressing)',
        'Nettoyage en profondeur des sièges (cuir/tissu)',
        'Nettoyage des vitres intérieures sans trace'
    ];

    const stdComplet = [
        '✨ Toutes les prestations de la formule Intérieur',
        '✨ Toutes les prestations de la formule Extérieur',
        'Soin protecteur pour plastiques intérieurs',
        'Cire de finition brillance sur carrosserie'
    ];

    const CARS = {
        citadine: { img: 'images/car-citadine.png', label: 'Citadine', subtitle: 'Clio, 208, Polo, Yaris...', icon: 'fa-car-side', services: { ext: stdExt, int: stdInt, complet: stdComplet } },
        berline:  { img: 'images/car-berline.png', label: 'Berline', subtitle: 'Série 3, Classe C, A4, Model 3...', icon: 'fa-car', services: { ext: stdExt, int: stdInt, complet: stdComplet } },
        suv:      { img: 'images/car-suv.png', label: 'SUV', subtitle: '3008, Tiguan, RAV4, Model Y...', icon: 'fa-truck-pickup', services: { ext: stdExt, int: stdInt, complet: stdComplet } },
        mono5:    { img: 'images/car-monospace.png', label: 'Monospace 5pl', subtitle: 'Scénic, Touran, Espace...', icon: 'fa-van-shuttle', services: { ext: stdExt, int: stdInt, complet: stdComplet } },
        mono7:    { img: 'images/car-monospace.png', label: 'Monospace 7pl', subtitle: 'Classe V, Espace 7, Touran 7...', icon: 'fa-bus', services: { ext: stdExt, int: stdInt, complet: stdComplet } },
        util:     { img: 'images/car-utilitaire.png', label: 'Utilitaire', subtitle: 'Sprinter, Master, Transit...', icon: 'fa-truck', services: { ext: ['Sur devis selon volume'], int: ['Sur devis selon volume'], complet: ['État du véhicule analysé sur place', 'Devis personnalisé garanti', 'Intervention sur site possible', 'Contactez-nous pour une estimation'] } }
    };

    const TARIFS = {
        citadine: { ext: 49, int: 79, complet: 119 },
        berline:  { ext: 59, int: 89, complet: 129 },
        suv:      { ext: 69, int: 99, complet: 139 },
        mono5:    { ext: 79, int: 109, complet: 149 },
        mono7:    { ext: 89, int: 119, complet: 159 },
        util:     { ext: null, int: null, complet: null }
    };

    let currentCar = null;
    let currentFormule = 'complet';
    let isAnimating = false;

    /* ── Build HTML ── */
    function createShowcase() {
        const container = document.getElementById('car-showcase-container');
        if (!container) return;

        const vehicleTabs = Object.entries(CARS).map(([key, car]) => `
            <button class="veh-tab" data-key="${key}" id="vtab-${key}" title="${car.subtitle}">
                <i class="fa-solid ${car.icon}"></i>
                ${car.label}
                ${key === 'util' ? '<span class="veh-devis">Devis</span>' : ''}
            </button>`).join('');

        container.innerHTML = `
        <div class="showcase-wrapper" id="showcase-wrapper">

            <!-- STEP 1 HEADER: Vehicle -->
            <div class="showcase-step-header">
                <div class="step-badge">01</div>
                <span class="step-title">Choisissez votre véhicule</span>
            </div>

            <!-- TOP: Vehicle navigation bar -->
            <nav class="vehicle-nav" id="vehicle-nav" role="tablist" aria-label="Sélection du véhicule">
                ${vehicleTabs}
            </nav>

            <!-- BODY: Stage + Panel -->
            <div class="showcase-body">

                <!-- LEFT: Car stage -->
                <div class="car-stage" id="car-stage">
                    <div class="stage-bg"></div>
                    <div class="spotlight spotlight-1"></div>
                    <div class="spotlight spotlight-2"></div>

                    <div class="car-platform">
                        <div class="car-image-wrap" id="car-image-wrap">
                            <img id="showcase-car-img" src="" alt="" class="showcase-car-img">
                            <div class="car-reflection"></div>
                        </div>
                        <div class="car-glow" id="car-glow"></div>
                        <div class="platform-ring"></div>
                    </div>

                    <div class="car-label-wrap">
                        <div class="car-label-name" id="car-label-name">—</div>
                        <div class="car-label-sub" id="car-label-sub">Sélectionnez un véhicule</div>
                    </div>

                    <canvas id="particle-canvas" class="particle-canvas"></canvas>
                </div>

                <!-- RIGHT: Services panel -->
                <div class="services-panel" id="services-panel">

                    <!-- Formule section header -->
                    <div class="panel-step-header">
                        <div class="step-badge step-badge--sm">02</div>
                        <span class="step-title--sm">Votre formule</span>
                    </div>

                    <!-- Formule pills -->
                    <div class="formule-pills" id="formule-tabs" role="tablist">
                        <button class="fpill fpill--featured active" data-f="complet" role="tab">
                            <div class="fpill-inner">
                                <i class="fa-solid fa-gem fpill-icon"></i>
                                <div class="fpill-info">
                                    <span class="fpill-name">Pack Complet</span>
                                    <span class="fpill-rec">Recommandé</span>
                                </div>
                                <span class="fpill-price" id="price-complet">—</span>
                            </div>
                        </button>
                        <button class="fpill" data-f="ext" role="tab">
                            <div class="fpill-inner">
                                <i class="fa-solid fa-spray-can fpill-icon"></i>
                                <div class="fpill-info">
                                    <span class="fpill-name">Extérieur</span>
                                    <span class="fpill-sub">Décontamination</span>
                                </div>
                                <span class="fpill-price" id="price-ext">—</span>
                            </div>
                        </button>
                        <button class="fpill" data-f="int" role="tab">
                            <div class="fpill-inner">
                                <i class="fa-solid fa-couch fpill-icon"></i>
                                <div class="fpill-info">
                                    <span class="fpill-name">Intérieur</span>
                                    <span class="fpill-sub">Pressing HD</span>
                                </div>
                                <span class="fpill-price" id="price-int">—</span>
                            </div>
                        </button>
                    </div>

                    <!-- Services list -->
                    <div class="services-list" id="services-list">
                        <div class="services-empty">
                            <i class="fa-solid fa-car-side"></i>
                            <p>Choisissez votre véhicule<br>pour voir les prestations</p>
                        </div>
                    </div>

                    <!-- Economy badge -->
                    <div class="economy-badge" id="economy-badge" style="display:none">
                        <i class="fa-solid fa-piggy-bank"></i>
                        <span id="economy-text"></span>
                    </div>

                    <!-- Price + CTA -->
                    <div class="price-summary">
                        <div>
                            <div class="price-label">Total estimé</div>
                            <div class="price-value" id="price-display">
                                — <span>€</span>
                            </div>
                        </div>
                        <a href="#" class="price-cta" id="showcase-cta">
                            <i class="fa-brands fa-whatsapp"></i>
                            Réserver
                        </a>
                    </div>
                </div>
            </div>
        </div>`;

        initVehicleTabs();
        initFormuleTabs();
        initParticles();
        init3DTilt();
    }

    /* ── Vehicle tabs ── */
    function initVehicleTabs() {
        document.querySelectorAll('.veh-tab').forEach(btn => {
            btn.addEventListener('click', () => {
                const key = btn.dataset.key;
                if (window.__alpineVehicule) window.__alpineVehicule(key);
                switchCar(key);
            });
        });
    }

    function setActiveVehicleTab(key) {
        document.querySelectorAll('.veh-tab').forEach(b => {
            b.classList.toggle('active', b.dataset.key === key);
            b.setAttribute('aria-selected', b.dataset.key === key);
        });
    }

    /* ── Formule pills ── */
    function initFormuleTabs() {
        document.querySelectorAll('.fpill').forEach(btn => {
            btn.addEventListener('click', () => {
                switchFormule(btn.dataset.f);
                if (window.__alpineFormule) window.__alpineFormule(btn.dataset.f);
            });
        });
    }

    function setActiveFormuleTab(f) {
        document.querySelectorAll('.fpill').forEach(b => b.classList.toggle('active', b.dataset.f === f));
    }

    /* ── Switch car ── */
    function switchCar(key) {
        if (isAnimating || currentCar === key) return;
        isAnimating = true;
        const data = CARS[key];
        if (!data) { isAnimating = false; return; }

        const wrap = document.getElementById('car-image-wrap');
        const img  = document.getElementById('showcase-car-img');
        const glow = document.getElementById('car-glow');

        // Exit animation
        wrap.style.transition = 'all 0.25s ease';
        wrap.style.opacity = '0';
        wrap.style.transform = 'translateX(-32px) scale(0.92)';

        setTimeout(() => {
            img.src = data.img;
            img.alt = data.label;
            document.getElementById('car-label-name').textContent = data.label;
            document.getElementById('car-label-sub').textContent = data.subtitle;
            glow.style.boxShadow = '0 0 60px 16px rgba(168,136,74,0.15)';

            wrap.style.transition = 'none';
            wrap.style.transform = 'translateX(32px) scale(0.92)';
            wrap.style.opacity = '0';

            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    wrap.style.transition = 'all 0.55s cubic-bezier(0.16,1,0.3,1)';
                    wrap.style.transform = 'translateX(0) scale(1)';
                    wrap.style.opacity = '1';
                });
            });

            currentCar = key;
            setActiveVehicleTab(key);
            updateServices(key, currentFormule);
            updatePrices(key);
            updateCTA(key);
            spawnParticles();
            isAnimating = false;

            // Sync Alpine.js state
            window.dispatchEvent(new CustomEvent('showcasecar', { detail: { key } }));
        }, 260);
    }

    /* ── Switch formule ── */
    function switchFormule(f) {
        currentFormule = f;
        setActiveFormuleTab(f);
        if (currentCar) {
            updateServices(currentCar, f);
            updatePriceDisplay(currentCar, f);
            updateCTA(currentCar);
        }
        updateEconomy(currentCar, f);

        // Sync Alpine.js state
        window.dispatchEvent(new CustomEvent('showcaseformule', { detail: { f } }));
    }

    /* ── Services list ── */
    function updateServices(carKey, formule) {
        const data = CARS[carKey];
        if (!data) return;
        const list = document.getElementById('services-list');
        const items = data.services[formule] || [];
        list.innerHTML = '';
        items.forEach((item, i) => {
            const el = document.createElement('div');
            el.className = 'service-item';
            el.innerHTML = `<i class="fa-solid fa-minus"></i><span>${item}</span>`;
            list.appendChild(el);
            setTimeout(() => el.classList.add('visible'), i * 45);
        });
    }

    /* ── Prices ── */
    function updatePrices(carKey) {
        const t = TARIFS[carKey];
        if (!t) return;
        const fmt = (v) => (v !== null && v !== undefined) ? v + '\u20ac' : 'Devis';
        document.getElementById('price-ext').textContent = fmt(t.ext);
        document.getElementById('price-int').textContent = fmt(t.int);
        document.getElementById('price-complet').textContent = fmt(t.complet);
        updatePriceDisplay(carKey, currentFormule);
        updateEconomy(carKey, currentFormule);
    }

    function updatePriceDisplay(carKey, formule) {
        const t = TARIFS[carKey];
        const el = document.getElementById('price-display');
        if (!el) return;
        const val = t && t[formule];
        if (val === null || val === undefined || !val) {
            el.innerHTML = 'Sur devis';
            return;
        }
        el.innerHTML = `${val} <span>\u20ac TTC</span>`;
    }

    function updateEconomy(carKey, formule) {
        const badge = document.getElementById('economy-badge');
        const t = TARIFS[carKey];
        if (!t || !t.ext || formule !== 'complet') { if (badge) badge.style.display = 'none'; return; }
        const saved = (t.ext + t.int) - t.complet;
        document.getElementById('economy-text').textContent = `${saved}€ économisés vs séparé`;
        badge.style.display = 'flex';
    }

    /* ── CTA Link (WhatsApp) ── */
    function updateCTA(carKey) {
        const cta = document.getElementById('showcase-cta');
        if (!cta || !carKey) return;
        const car = CARS[carKey];
        const t   = TARIFS[carKey];
        const formuleLabels = { complet: 'Pack Complet', ext: 'Ext\u00e9rieur', int: 'Int\u00e9rieur' };
        const prixStr = (t && t[currentFormule] !== null && t[currentFormule] !== undefined)
            ? t[currentFormule] + '\u20ac'
            : 'Sur devis';
        const msg = encodeURIComponent(
            'Bonjour Continental Detailing, je souhaite r\u00e9server :\n' +
            '\uD83D\uDE97 V\u00e9hicule : ' + (car ? car.label : carKey) + '\n' +
            '\u2728 Formule : ' + (formuleLabels[currentFormule] || currentFormule) + '\n' +
            '\uD83D\uDCB0 Estimation : ' + prixStr
        );
        cta.href = 'https://wa.me/33750875964?text=' + msg;
        cta.target = '_blank';
        cta.rel    = 'noopener noreferrer';
    }

    /* ── Particles ── */
    let pCanvas, pCtx, particles = [];

    function initParticles() {
        pCanvas = document.getElementById('particle-canvas');
        if (!pCanvas) return;
        pCtx = pCanvas.getContext('2d');
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        animateParticles();
    }

    function resizeCanvas() {
        const stage = document.getElementById('car-stage');
        if (!stage || !pCanvas) return;
        pCanvas.width = stage.offsetWidth;
        pCanvas.height = stage.offsetHeight;
    }

    function spawnParticles() {
        if (!pCanvas) return;
        const cx = pCanvas.width / 2;
        const cy = pCanvas.height * 0.5;
        for (let i = 0; i < 20; i++) {
            particles.push({
                x: cx + (Math.random() - 0.5) * 140,
                y: cy,
                vx: (Math.random() - 0.5) * 2.5,
                vy: -(Math.random() * 2.5 + 0.8),
                size: Math.random() * 2.5 + 0.8,
                alpha: 1,
                color: Math.random() > 0.5 ? '#A8884A' : '#C4A55D'
            });
        }
    }

    function animateParticles() {
        if (!pCtx || !pCanvas) { requestAnimationFrame(animateParticles); return; }
        pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
        particles = particles.filter(p => p.alpha > 0.01);
        particles.forEach(p => {
            p.x += p.vx; p.y += p.vy; p.vy += 0.03; p.alpha *= 0.97;
            pCtx.beginPath();
            pCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            pCtx.fillStyle = p.color + Math.floor(p.alpha * 255).toString(16).padStart(2, '0');
            pCtx.fill();
        });
        requestAnimationFrame(animateParticles);
    }

    /* ── 3D Tilt ── */
    function init3DTilt() {
        document.addEventListener('mousemove', (e) => {
            const stage = document.getElementById('car-stage');
            const wrap  = document.getElementById('car-image-wrap');
            if (!stage || !wrap || !currentCar) return;
            const rect = stage.getBoundingClientRect();
            if (e.clientX >= rect.left && e.clientX <= rect.right &&
                e.clientY >= rect.top  && e.clientY <= rect.bottom) {
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top)  / rect.height - 0.5;
                wrap.style.transform = `perspective(900px) rotateY(${x * 9}deg) rotateX(${-y * 4.5}deg) scale(1.02)`;
            } else {
                wrap.style.transform = '';
            }
        });
    }

    /* ── Boot ── */
    document.addEventListener('DOMContentLoaded', () => {
        createShowcase();
        setTimeout(() => switchCar('citadine'), 350);
    });

    /* ── Public API ── */
    window.showcaseSwitchCar     = switchCar;
    window.showcaseSwitchFormule = switchFormule;

})();
