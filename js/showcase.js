/**
 * Continental Detailing — 3D Car Showcase Engine v2
 * Vehicle selector integrated inside the left panel
 */
(function() {
    'use strict';

    const CARS = {
        citadine: {
            img: 'images/car-citadine.png',
            label: 'Citadine',
            subtitle: 'Clio, 208, Polo, Yaris...',
            icon: 'fa-car-side',
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
            icon: 'fa-car',
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
            icon: 'fa-truck-pickup',
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
            icon: 'fa-van-shuttle',
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
            icon: 'fa-bus',
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
            icon: 'fa-truck',
            services: {
                ext: ['Snow Foam grand volume', 'Lavage carrosserie utilitaire', 'Décontamination jantes doubles', 'Nettoyage rehausses & crocs', 'Traitement protection carrosserie'],
                int: ['Aspiration plancher de charge', 'Pressing siège conducteur', 'Dégraissage tableau de bord', 'Nettoyage parois internes', 'Désinfection habitacle'],
                complet: ['Traitement complet sur devis', 'Selon volume L1/L2/L3', 'État du véhicule analysé', 'Devis personnalisé garanti', 'Intervention sur site', 'Contact pour estimation']
            }
        }
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

    function createShowcase() {
        const container = document.getElementById('car-showcase-container');
        if (!container) return;

        const vehicleButtons = Object.entries(CARS).map(([key, car]) => `
            <button class="veh-btn" data-key="${key}" id="vbtn-${key}">
                <i class="fa-solid ${car.icon}"></i>
                <span>${car.label}</span>
                ${key === 'util' ? '<em>Devis</em>' : ''}
            </button>
        `).join('');

        container.innerHTML = `
        <div class="showcase-wrapper" id="showcase-wrapper">

            <!-- LEFT: Car Stage + Vehicle Selector -->
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
                    <div class="car-label-name" id="car-label-name">Sélectionnez</div>
                    <div class="car-label-sub" id="car-label-sub">votre véhicule ci-dessous</div>
                </div>

                <!-- VEHICLE SELECTOR — integrated in stage -->
                <div class="vehicle-selector" id="vehicle-selector">
                    ${vehicleButtons}
                </div>

                <canvas id="particle-canvas" class="particle-canvas"></canvas>
            </div>

            <!-- RIGHT: Services Panel -->
            <div class="services-panel" id="services-panel">

                <div class="panel-eyebrow">Prestations incluses</div>

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

        initVehicleButtons();
        initTabs();
        initParticles();
    }

    function initVehicleButtons() {
        document.querySelectorAll('.veh-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const key = btn.dataset.key;
                // Update Alpine state
                if (window.__alpineVehicule) window.__alpineVehicule(key);
                switchCar(key);
            });
        });
    }

    function setActiveVehicleBtn(key) {
        document.querySelectorAll('.veh-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('vbtn-' + key);
        if (btn) btn.classList.add('active');
    }

    function initTabs() {
        document.querySelectorAll('.ftab').forEach(btn => {
            btn.addEventListener('click', () => {
                switchFormule(btn.dataset.f);
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

        wrap.style.transform = 'translateX(-50px) rotateY(-12deg) scale(0.88)';
        wrap.style.opacity = '0';

        setTimeout(() => {
            img.src = data.img;
            img.alt = data.label;
            labelName.textContent = data.label;
            labelSub.textContent = data.subtitle;
            glow.style.boxShadow = '0 0 80px 20px rgba(168,136,74,0.2)';

            wrap.style.transition = 'none';
            wrap.style.transform = 'translateX(50px) rotateY(12deg) scale(0.88)';
            wrap.style.opacity = '0';

            requestAnimationFrame(() => {
                wrap.style.transition = 'all 0.7s cubic-bezier(0.16,1,0.3,1)';
                wrap.style.transform = 'translateX(0) rotateY(0deg) scale(1)';
                wrap.style.opacity = '1';
            });

            currentCar = key;
            setActiveVehicleBtn(key);
            updateServices(key, currentFormule);
            updatePrices(key);
            spawnParticles();
            isAnimating = false;
        }, 320);
    }

    function switchFormule(f) {
        currentFormule = f;
        if (currentCar) updateServices(currentCar, f);
        document.querySelectorAll('.ftab').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.f === f);
        });
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
            el.style.transitionDelay = `${i * 0.06}s`;
            el.innerHTML = `<i class="fa-solid fa-check-circle"></i><span>${item}</span>`;
            list.appendChild(el);
            requestAnimationFrame(() => setTimeout(() => el.classList.add('visible'), i * 40));
        });
    }

    function updatePrices(carKey) {
        const t = TARIFS[carKey];
        if (!t) return;
        document.getElementById('price-ext').textContent = t.ext ? t.ext + '€' : 'Devis';
        document.getElementById('price-int').textContent = t.int ? t.int + '€' : 'Devis';
        document.getElementById('price-complet').textContent = t.complet ? t.complet + '€' : 'Devis';
        updateEconomy(carKey, currentFormule);
    }

    function updateEconomy(carKey, formule) {
        const badge = document.getElementById('economy-badge');
        const t = TARIFS[carKey];
        if (!t || !t.ext || formule !== 'complet') { if(badge) badge.style.display = 'none'; return; }
        const saved = (t.ext + t.int) - t.complet;
        document.getElementById('economy-text').textContent = `Vous économisez ${saved}€ vs. séparé`;
        badge.style.display = 'flex';
    }

    // ---- Particles ----
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
        for (let i = 0; i < 24; i++) {
            particles.push({
                x: cx + (Math.random() - 0.5) * 160,
                y: cy,
                vx: (Math.random() - 0.5) * 3,
                vy: -(Math.random() * 3 + 1),
                size: Math.random() * 3 + 1,
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
            p.x += p.vx; p.y += p.vy; p.vy += 0.04; p.alpha *= 0.965;
            pCtx.beginPath();
            pCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            pCtx.fillStyle = p.color + Math.floor(p.alpha * 255).toString(16).padStart(2, '0');
            pCtx.fill();
        });
        requestAnimationFrame(animateParticles);
    }

    // ---- 3D Tilt ----
    document.addEventListener('DOMContentLoaded', () => {
        createShowcase();

        document.addEventListener('mousemove', (e) => {
            const stage = document.getElementById('car-stage');
            const wrap = document.getElementById('car-image-wrap');
            if (!stage || !wrap || !currentCar) return;
            const rect = stage.getBoundingClientRect();
            if (e.clientX >= rect.left && e.clientX <= rect.right &&
                e.clientY >= rect.top && e.clientY <= rect.bottom) {
                const x = (e.clientX - rect.left) / rect.width - 0.5;
                const y = (e.clientY - rect.top) / rect.height - 0.5;
                wrap.style.transform = `perspective(900px) rotateY(${x * 10}deg) rotateX(${-y * 5}deg) scale(1.02)`;
            } else {
                wrap.style.transform = '';
            }
        });

        // Auto-select citadine on load
        setTimeout(() => switchCar('citadine'), 400);
    });

    // Exposed API
    window.showcaseSwitchCar = switchCar;
    window.showcaseSwitchFormule = switchFormule;
})();
