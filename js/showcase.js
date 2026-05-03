/**
 * Continental Detailing — 3D Car Showcase Engine
 */
(function() {
    'use strict';

    const CARS = {
        citadine: {
            img: 'images/car-citadine.png',
            label: 'Citadine',
            subtitle: 'Clio, 208, Polo, Yaris...',
            color: '#C9A84C',
            services: {
                ext: ['Prélavage Snow Foam', 'Lavage 2 seaux microfibre', 'Décontamination jantes', 'Dressing pneus', 'Séchage sécurisé'],
                int: ['Aspiration chirurgicale', 'Pressing injection/extraction', 'Dégraissage au pinceau', 'Protection Anti-UV', 'Soin des cuirs'],
                complet: ['Snow Foam + Lavage 2 seaux', 'Décontamination jantes + pneus', 'Aspiration chirurgicale', 'Pressing profondeur', 'Dégraissage plastiques', 'Soin cuirs & vitres']
            }
        },
        berline: {
            img: 'images/car-berline.png',
            label: 'Berline',
            subtitle: 'Série 3, Classe C, A4, Model 3...',
            color: '#C9A84C',
            services: {
                ext: ['Prélavage Snow Foam', 'Lavage 2 seaux microfibre', 'Décontamination jantes & freins', 'Détails pinceau calandre', 'Dressing pneus premium'],
                int: ['Aspiration sièges & coffre', 'Pressing injection/extraction', 'Dégraissage commodos', 'Protection Anti-UV plastiques', 'Finition vitres sans trace'],
                complet: ['Snow Foam + Lavage complet', 'Décontamination totale', 'Aspiration + pressing HD', 'Plastiques + cuirs traités', 'Vitres dégraissées', 'Dressing pneus']
            }
        },
        suv: {
            img: 'images/car-suv.png',
            label: 'SUV',
            subtitle: '3008, Tiguan, RAV4, Model Y...',
            color: '#C9A84C',
            services: {
                ext: ['Snow Foam grande surface', 'Lavage 2 seaux spécialisé', 'Décontamination jantes', 'Nettoyage soubassements', 'Dressing pneus 4x4'],
                int: ['Aspiration 5 places + coffre', 'Pressing banquettes arrière', 'Dégraissage tableau de bord', 'Protection UV renforcée', 'Soin cuirs & alcantara'],
                complet: ['Snow Foam + Lavage intégral', 'Décontamination jantes HD', 'Aspiration coffre + habitacle', 'Pressing profond 5 places', 'Plastiques + cuirs soignés', 'Vitres panoramiques traitées']
            }
        },
        mono5: {
            img: 'images/car-monospace.png',
            label: 'Monospace 5pl',
            subtitle: 'Scénic, Touran, Espace...',
            color: '#C9A84C',
            services: {
                ext: ['Snow Foam carrosserie longue', 'Lavage 2 seaux grande surface', 'Décontamination 4 jantes', 'Joints & trappes nettoyés', 'Dressing pneus complet'],
                int: ['Aspiration 5 places + coffre', 'Pressing tapis & sièges', 'Dégraissage panneaux portes', 'Protection plastiques UV', 'Vitres coulissantes traitées'],
                complet: ['Snow Foam + Lavage XL', 'Décontamination jantes totale', 'Aspiration 5pl + grand coffre', 'Pressing tapis longue durée', 'Plastiques + cuirs traités', 'Vitres sans trace']
            }
        },
        mono7: {
            img: 'images/car-monospace.png',
            label: 'Monospace 7pl',
            subtitle: 'Classe V, Espace 7, Touran 7...',
            color: '#C9A84C',
            services: {
                ext: ['Snow Foam carrosserie XXL', 'Lavage 2 seaux surface totale', 'Décontamination jantes', 'Nettoyage soubassements longs', 'Dressing pneus 7pl'],
                int: ['Aspiration 7 places + coffre', 'Pressing rang 2 & rang 3', 'Dégraissage tableau de bord', 'Protection UV toute surface', 'Soin cuirs 7 places'],
                complet: ['Snow Foam + Lavage XXL', 'Décontamination totale', 'Aspiration 7pl profonde', 'Pressing tapis 3 rangs', 'Plastiques & cuirs soignés', 'Vitres latérales traitées']
            }
        },
        util: {
            img: 'images/car-utilitaire.png',
            label: 'Utilitaire',
            subtitle: 'Sprinter, Master, Transit...',
            color: '#C9A84C',
            services: {
                ext: ['Snow Foam grand volume', 'Lavage carrosserie utilitaire', 'Décontamination jantes doubles', 'Nettoyage rehausses & crocs', 'Traitement protection carrosserie'],
                int: ['Aspiration plancher de charge', 'Pressing siège conducteur', 'Dégraissage tableau de bord', 'Nettoyage parois internes', 'Désinfection habitacle'],
                complet: ['Traitement complet sur devis', 'Selon volume L1/L2/L3', 'État du véhicule analysé', 'Devis personnalisé garanti', 'Intervention sur site', 'Contact pour estimation']
            }
        }
    };

    let currentCar = null;
    let currentFormule = 'complet';
    let isAnimating = false;

    function createShowcase() {
        const container = document.getElementById('car-showcase-container');
        if (!container) return;

        container.innerHTML = `
        <div class="showcase-wrapper" id="showcase-wrapper">
            <!-- LEFT: Car Stage -->
            <div class="car-stage" id="car-stage">
                <div class="stage-bg"></div>
                <div class="spotlight spotlight-1"></div>
                <div class="spotlight spotlight-2"></div>
                <div class="car-platform">
                    <div class="car-image-wrap" id="car-image-wrap">
                        <img id="showcase-car-img" src="" alt="" class="showcase-car-img">
                        <div class="car-reflection" id="car-reflection"></div>
                    </div>
                    <div class="car-glow" id="car-glow"></div>
                    <div class="platform-ring"></div>
                </div>
                <div class="car-label-wrap" id="car-label-wrap">
                    <div class="car-label-name" id="car-label-name">—</div>
                    <div class="car-label-sub" id="car-label-sub">Sélectionnez un véhicule</div>
                </div>
                <canvas id="particle-canvas" class="particle-canvas"></canvas>
            </div>

            <!-- RIGHT: Services Panel -->
            <div class="services-panel" id="services-panel">
                <div class="formule-tabs" id="formule-tabs">
                    <button class="ftab active" data-f="complet">
                        <i class="fa-solid fa-gem"></i>
                        <span>Pack Complet</span>
                        <span class="ftab-badge" id="price-complet">—</span>
                    </button>
                    <button class="ftab" data-f="ext">
                        <i class="fa-solid fa-spray-can"></i>
                        <span>Extérieur</span>
                        <span class="ftab-badge" id="price-ext">—</span>
                    </button>
                    <button class="ftab" data-f="int">
                        <i class="fa-solid fa-couch"></i>
                        <span>Intérieur</span>
                        <span class="ftab-badge" id="price-int">—</span>
                    </button>
                </div>

                <div class="services-list" id="services-list">
                    <div class="services-empty">
                        <i class="fa-solid fa-car-side"></i>
                        <p>Sélectionnez un véhicule<br>pour voir les prestations</p>
                    </div>
                </div>

                <div class="economy-badge" id="economy-badge" style="display:none">
                    <i class="fa-solid fa-piggy-bank"></i>
                    <span id="economy-text">Économie avec le pack</span>
                </div>
            </div>
        </div>`;

        initTabs();
        initParticles();

        // Listen to Alpine vehicule changes
        document.addEventListener('vehiculeChanged', (e) => switchCar(e.detail));
        document.addEventListener('formuleChanged', (e) => switchFormule(e.detail));
    }

    function initTabs() {
        document.querySelectorAll('.ftab').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.ftab').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                switchFormule(btn.dataset.f);

                // Sync Alpine
                if (window.__alpineFormule) window.__alpineFormule(btn.dataset.f);
            });
        });
    }

    function switchCar(key) {
        if (isAnimating || currentCar === key) return;
        isAnimating = true;

        const data = CARS[key];
        if (!data) { isAnimating = false; return; }

        const wrap = document.getElementById('car-image-wrap');
        const img = document.getElementById('showcase-car-img');
        const labelName = document.getElementById('car-label-name');
        const labelSub = document.getElementById('car-label-sub');
        const glow = document.getElementById('car-glow');

        // Exit animation
        wrap.style.transform = 'translateX(-60px) rotateY(-15deg) scale(0.85)';
        wrap.style.opacity = '0';

        setTimeout(() => {
            img.src = data.img;
            img.alt = data.label;
            labelName.textContent = data.label;
            labelSub.textContent = data.subtitle;
            glow.style.boxShadow = `0 0 80px 20px rgba(201,168,76,0.25)`;

            // Enter animation
            wrap.style.transition = 'none';
            wrap.style.transform = 'translateX(60px) rotateY(15deg) scale(0.85)';
            wrap.style.opacity = '0';

            requestAnimationFrame(() => {
                wrap.style.transition = 'all 0.7s cubic-bezier(0.16,1,0.3,1)';
                wrap.style.transform = 'translateX(0) rotateY(0deg) scale(1)';
                wrap.style.opacity = '1';
            });

            currentCar = key;
            updateServices(key, currentFormule);
            updatePrices(key);
            spawnParticles();
            isAnimating = false;
        }, 350);
    }

    function switchFormule(f) {
        currentFormule = f;
        if (currentCar) updateServices(currentCar, f);

        // Update tab badge highlight
        document.querySelectorAll('.ftab').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.f === f);
        });

        // Update economy badge
        updateEconomy(currentCar, f);
    }

    function updateServices(carKey, formule) {
        const data = CARS[carKey];
        if (!data) return;
        const list = document.getElementById('services-list');
        const items = data.services[formule] || [];

        list.innerHTML = '';
        items.forEach((item, i) => {
            const el = document.createElement('div');
            el.className = 'service-item';
            el.style.animationDelay = `${i * 0.07}s`;
            el.innerHTML = `<i class="fa-solid fa-check-circle"></i><span>${item}</span>`;
            list.appendChild(el);
            // Trigger animation
            requestAnimationFrame(() => el.classList.add('visible'));
        });
    }

    function updatePrices(carKey) {
        const tarifs = {
            citadine: { ext: 49, int: 79, complet: 119 },
            berline:  { ext: 59, int: 89, complet: 129 },
            suv:      { ext: 69, int: 99, complet: 139 },
            mono5:    { ext: 79, int: 109, complet: 149 },
            mono7:    { ext: 89, int: 119, complet: 159 },
            util:     { ext: null, int: null, complet: null }
        };
        const t = tarifs[carKey];
        if (!t) return;
        document.getElementById('price-ext').textContent = t.ext ? t.ext + '€' : 'Devis';
        document.getElementById('price-int').textContent = t.int ? t.int + '€' : 'Devis';
        document.getElementById('price-complet').textContent = t.complet ? t.complet + '€' : 'Devis';
        updateEconomy(carKey, currentFormule);
    }

    function updateEconomy(carKey, formule) {
        const tarifs = {
            citadine: { ext: 49, int: 79, complet: 119 },
            berline:  { ext: 59, int: 89, complet: 129 },
            suv:      { ext: 69, int: 99, complet: 139 },
            mono5:    { ext: 79, int: 109, complet: 149 },
            mono7:    { ext: 89, int: 119, complet: 159 }
        };
        const badge = document.getElementById('economy-badge');
        const t = tarifs[carKey];
        if (!t || formule !== 'complet') { badge.style.display = 'none'; return; }
        const saved = (t.ext + t.int) - t.complet;
        document.getElementById('economy-text').textContent = `Économie de ${saved}€ avec le Pack Complet`;
        badge.style.display = 'flex';
    }

    // ---- Particle System ----
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
        const cy = pCanvas.height * 0.6;
        for (let i = 0; i < 30; i++) {
            particles.push({
                x: cx + (Math.random() - 0.5) * 200,
                y: cy,
                vx: (Math.random() - 0.5) * 4,
                vy: -(Math.random() * 4 + 1),
                size: Math.random() * 4 + 1,
                alpha: 1,
                color: Math.random() > 0.5 ? '#C9A84C' : '#DFC068'
            });
        }
    }

    function animateParticles() {
        if (!pCtx || !pCanvas) { requestAnimationFrame(animateParticles); return; }
        pCtx.clearRect(0, 0, pCanvas.width, pCanvas.height);
        particles = particles.filter(p => p.alpha > 0.01);
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.05;
            p.alpha *= 0.96;
            pCtx.beginPath();
            pCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            pCtx.fillStyle = p.color + Math.floor(p.alpha * 255).toString(16).padStart(2, '0');
            pCtx.fill();
        });
        requestAnimationFrame(animateParticles);
    }

    // ---- Init ----
    document.addEventListener('DOMContentLoaded', () => {
        createShowcase();

        // Hover 3D tilt on car
        document.addEventListener('mousemove', (e) => {
            const stage = document.getElementById('car-stage');
            const wrap = document.getElementById('car-image-wrap');
            if (!stage || !wrap || !currentCar) return;
            const rect = stage.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            if (e.clientX >= rect.left && e.clientX <= rect.right &&
                e.clientY >= rect.top && e.clientY <= rect.bottom) {
                wrap.style.transform = `perspective(1000px) rotateY(${x * 12}deg) rotateX(${-y * 6}deg) scale(1.02)`;
            } else {
                wrap.style.transform = '';
            }
        });
    });

    // Expose globally for Alpine.js bridge
    window.showcaseSwitchCar = switchCar;
    window.showcaseSwitchFormule = switchFormule;
})();
