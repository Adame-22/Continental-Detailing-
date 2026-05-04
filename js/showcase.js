/**
 * Continental Detailing — Showcase Engine v3
 * Layout: vehicle nav tabs (top) | car stage (left) | services panel (right)
 */
(function () {
    'use strict';

    const CARS = {
        citadine: { img: 'images/car-citadine.png', label: 'Citadine', subtitle: 'Clio, 208, Polo, Yaris...', icon: 'fa-car-side', services: { ext: ['Prélavage Snow Foam', 'Lavage 2 seaux microfibre', 'Décontamination jantes', 'Dressing pneus', 'Séchage sécurisé'], int: ['Aspiration chirurgicale', 'Pressing injection/extraction', 'Dégraissage au pinceau', 'Protection Anti-UV', 'Soin des cuirs'], complet: ['Snow Foam + Lavage 2 seaux', 'Décontamination jantes & pneus', 'Aspiration chirurgicale', 'Pressing profondeur', 'Dégraissage plastiques', 'Soin cuirs & vitres'] } },
        berline:  { img: 'images/car-berline.png', label: 'Berline', subtitle: 'Série 3, Classe C, A4, Model 3...', icon: 'fa-car', services: { ext: ['Prélavage Snow Foam', 'Lavage 2 seaux microfibre', 'Décontamination jantes & freins', 'Détails pinceau calandre', 'Dressing pneus premium'], int: ['Aspiration sièges & coffre', 'Pressing injection/extraction', 'Dégraissage commodos', 'Protection Anti-UV plastiques', 'Finition vitres sans trace'], complet: ['Snow Foam + Lavage complet', 'Décontamination totale', 'Aspiration + pressing HD', 'Plastiques + cuirs traités', 'Vitres dégraissées', 'Dressing pneus'] } },
        suv:      { img: 'images/car-suv.png', label: 'SUV', subtitle: '3008, Tiguan, RAV4, Model Y...', icon: 'fa-truck-pickup', services: { ext: ['Snow Foam grande surface', 'Lavage 2 seaux spécialisé', 'Décontamination jantes', 'Nettoyage soubassements', 'Dressing pneus 4x4'], int: ['Aspiration 5 places + coffre', 'Pressing banquettes arrière', 'Dégraissage tableau de bord', 'Protection UV renforcée', 'Soin cuirs & alcantara'], complet: ['Snow Foam + Lavage intégral', 'Décontamination jantes HD', 'Aspiration coffre + habitacle', 'Pressing profond 5 places', 'Plastiques + cuirs soignés', 'Vitres panoramiques'] } },
        mono5:    { img: 'images/car-monospace.png', label: 'Monospace 5pl', subtitle: 'Scénic, Touran, Espace...', icon: 'fa-van-shuttle', services: { ext: ['Snow Foam carrosserie longue', 'Lavage 2 seaux grande surface', 'Décontamination 4 jantes', 'Joints & trappes nettoyés', 'Dressing pneus complet'], int: ['Aspiration 5 places + coffre', 'Pressing tapis & sièges', 'Dégraissage panneaux portes', 'Protection plastiques UV', 'Vitres coulissantes traitées'], complet: ['Snow Foam + Lavage XL', 'Décontamination jantes totale', 'Aspiration 5pl + grand coffre', 'Pressing tapis longue durée', 'Plastiques + cuirs traités', 'Vitres sans trace'] } },
        mono7:    { img: 'images/car-monospace.png', label: 'Monospace 7pl', subtitle: 'Classe V, Espace 7, Touran 7...', icon: 'fa-bus', services: { ext: ['Snow Foam carrosserie XXL', 'Lavage 2 seaux surface totale', 'Décontamination jantes', 'Nettoyage soubassements longs', 'Dressing pneus 7pl'], int: ['Aspiration 7 places + coffre', 'Pressing rang 2 & rang 3', 'Dégraissage tableau de bord', 'Protection UV toute surface', 'Soin cuirs 7 places'], complet: ['Snow Foam + Lavage XXL', 'Décontamination totale', 'Aspiration 7pl profonde', 'Pressing tapis 3 rangs', 'Plastiques & cuirs soignés', 'Vitres latérales traitées'] } },
        util:     { img: 'images/car-utilitaire.png', label: 'Utilitaire', subtitle: 'Sprinter, Master, Transit...', icon: 'fa-truck', services: { ext: ['Snow Foam grand volume', 'Lavage carrosserie utilitaire', 'Décontamination jantes doubles', 'Nettoyage rehausses & crocs', 'Protection carrosserie'], int: ['Aspiration plancher de charge', 'Pressing siège conducteur', 'Dégraissage tableau de bord', 'Nettoyage parois internes', 'Désinfection habitacle'], complet: ['Traitement complet sur devis', 'Selon volume L1/L2/L3', 'État du véhicule analysé', 'Devis personnalisé garanti', 'Intervention sur site', 'Contact pour estimation'] } }
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

                    <!-- Formule tabs -->
                    <div class="formule-tabs" id="formule-tabs" role="tablist">
                        <button class="ftab active" data-f="complet" role="tab">
                            <i class="fa-solid fa-gem"></i>
                            Pack Complet
                            <span class="ftab-rec">Best</span>
                            <span class="ftab-price" id="price-complet">—</span>
                        </button>
                        <button class="ftab" data-f="ext" role="tab">
                            <i class="fa-solid fa-spray-can"></i>
                            Extérieur
                            <span class="ftab-price" id="price-ext">—</span>
                        </button>
                        <button class="ftab" data-f="int" role="tab">
                            <i class="fa-solid fa-couch"></i>
                            Intérieur
                            <span class="ftab-price" id="price-int">—</span>
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

    /* ── Formule tabs ── */
    function initFormuleTabs() {
        document.querySelectorAll('.ftab').forEach(btn => {
            btn.addEventListener('click', () => {
                switchFormule(btn.dataset.f);
                if (window.__alpineFormule) window.__alpineFormule(btn.dataset.f);
            });
        });
    }

    function setActiveFormuleTab(f) {
        document.querySelectorAll('.ftab').forEach(b => b.classList.toggle('active', b.dataset.f === f));
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

        // Exit
        wrap.style.opacity = '0';
        wrap.style.transform = 'translateX(-40px) scale(0.9)';

        setTimeout(() => {
            img.src = data.img;
            img.alt = data.label;
            document.getElementById('car-label-name').textContent = data.label;
            document.getElementById('car-label-sub').textContent = data.subtitle;
            glow.style.boxShadow = '0 0 60px 16px rgba(168,136,74,0.15)';

            wrap.style.transition = 'none';
            wrap.style.transform = 'translateX(40px) scale(0.9)';
            wrap.style.opacity = '0';

            requestAnimationFrame(() => {
                wrap.style.transition = 'all 0.6s cubic-bezier(0.16,1,0.3,1)';
                wrap.style.transform = 'translateX(0) scale(1)';
                wrap.style.opacity = '1';
            });

            currentCar = key;
            setActiveVehicleTab(key);
            updateServices(key, currentFormule);
            updatePrices(key);
            updateCTA(key);
            spawnParticles();
            isAnimating = false;
        }, 280);
    }

    /* ── Switch formule ── */
    function switchFormule(f) {
        currentFormule = f;
        setActiveFormuleTab(f);
        if (currentCar) { updateServices(currentCar, f); updatePriceDisplay(currentCar, f); }
        updateEconomy(currentCar, f);
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
        const fmt = (v) => v ? v + '€' : 'Devis';
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
        if (!t || !t[formule]) { el.innerHTML = 'Devis <span></span>'; return; }
        el.innerHTML = `${t[formule]} <span>€ TTC</span>`;
    }

    function updateEconomy(carKey, formule) {
        const badge = document.getElementById('economy-badge');
        const t = TARIFS[carKey];
        if (!t || !t.ext || formule !== 'complet') { if (badge) badge.style.display = 'none'; return; }
        const saved = (t.ext + t.int) - t.complet;
        document.getElementById('economy-text').textContent = `${saved}€ économisés vs séparé`;
        badge.style.display = 'flex';
    }

    /* ── CTA Link ── */
    function updateCTA(carKey) {
        const cta = document.getElementById('showcase-cta');
        if (!cta) return;
        const t = TARIFS[carKey];
        const price = t && t[currentFormule] ? t[currentFormule] + '€' : 'devis';
        const msg = encodeURIComponent(`Bonjour Continental Detailing, je souhaite réserver :\n🚗 Véhicule : ${CARS[carKey]?.label}\n💰 Estimation : ${price}`);
        cta.href = `https://wa.me/33750875964?text=${msg}`;
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
