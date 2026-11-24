/**
 * Simulateur — petites interactions : le prix « saute » quand il change,
 * la voiture glisse à chaque changement de véhicule, l'onglet choisi se
 * recentre, et le téléphone vibre brièvement à chaque sélection (Android).
 */
(function () {
    'use strict';
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function replay(el, cls) {
        if (!el || reduced) return;
        el.classList.remove(cls);
        void el.offsetWidth; // relance l'animation
        el.classList.add(cls);
    }

    function watchText(el, cls) {
        if (!el) return;
        var last = el.textContent;
        new MutationObserver(function () {
            if (el.textContent === last) return;
            last = el.textContent;
            replay(el, cls);
        }).observe(el, { childList: true, characterData: true, subtree: true });
    }

    function ready() {
        document.querySelectorAll('.sim-bar p.text-2xl, .sim-total__price b').forEach(function (el) { watchText(el, 'price-pop'); });

        var img = document.getElementById('showcase-car-img');
        if (img) {
            new MutationObserver(function () { replay(img, 'car-in'); })
                .observe(img, { attributes: true, attributeFilter: ['src'] });
        }

        document.addEventListener('click', function (e) {
            var tab = e.target.closest('.veh-tab');
            var pick = tab || e.target.closest('.fpill, .sim-side button');
            if (!pick) return;
            if (navigator.vibrate) { try { navigator.vibrate(8); } catch (err) { /* refusé */ } }
            if (tab && tab.scrollIntoView) tab.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', inline: 'center', block: 'nearest' });
        });
    }

    // Le simulateur est construit par showcase.js : on attend qu'il soit en place.
    var tries = 0;
    (function wait() {
        if (document.getElementById('showcase-car-img') || tries++ > 40) return ready();
        setTimeout(wait, 100);
    })();
})();
