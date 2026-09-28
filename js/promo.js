/**
 * Continental Detailing — seasonal offer.
 * Single source of truth for the current promotion. Loaded in <head> (sync)
 * so the banner and prices are right on first paint. After END the offer
 * switches itself off everywhere (banner, popup, countdowns, discounted
 * prices): no code change needed on November 1st.
 */
(function () {
    'use strict';

    var LABEL = 'Offre Automne';
    var RATE  = 0.20;
    // 31 October 2026, 23:59:59 Paris time (CET, summer time ends 25 Oct)
    var END   = new Date('2026-10-31T23:59:59+01:00');

    var POPUP_DELAY_MS   = 2500;
    var POPUP_REPEAT_MS  = 24 * 60 * 60 * 1000; // at most once a day per visitor
    var POPUP_STORAGE    = 'cdPromoPopupSeenAt';

    var active = Date.now() <= END.getTime();

    function apply(value) {
        if (!active || typeof value !== 'number' || !value) return value;
        return Math.round(value * (1 - RATE));
    }

    function remaining() {
        var ms = Math.max(0, END.getTime() - Date.now());
        return {
            total: ms,
            d: Math.floor(ms / 86400000),
            h: Math.floor(ms / 3600000) % 24,
            m: Math.floor(ms / 60000) % 60,
            s: Math.floor(ms / 1000) % 60
        };
    }

    function daysLeft() {
        return Math.max(0, Math.ceil((END.getTime() - Date.now()) / 86400000));
    }

    function track(name) {
        if (typeof window.gtag === 'function') window.gtag('event', name, { promo: LABEL });
    }

    window.PROMO = {
        active: active,
        label: LABEL,
        rate: RATE,
        percent: Math.round(RATE * 100),
        end: END,
        apply: apply,
        daysLeft: daysLeft,
        remaining: remaining
    };

    if (!active) return;

    document.documentElement.classList.add('promo-on');

    function euros(v) { return v + '€'; }
    var endLabel = END.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', timeZone: 'Europe/Paris' });

    /* ── Live countdown (any [data-promo-countdown] on the page) ── */
    function pad(n) { return (n < 10 ? '0' : '') + n; }

    function renderCountdowns() {
        var r = remaining();
        var parts = [[r.d, r.d > 1 ? 'jours' : 'jour'], [pad(r.h), 'h'], [pad(r.m), 'min'], [pad(r.s), 's']];
        var html = parts.map(function (p) {
            return '<span class="cd-box"><b>' + p[0] + '</b><small>' + p[1] + '</small></span>';
        }).join('');
        document.querySelectorAll('[data-promo-countdown]').forEach(function (el) {
            el.innerHTML = html;
        });
    }

    /* ── Arrival popup ── */
    function popupRecentlySeen() {
        try {
            var t = parseInt(localStorage.getItem(POPUP_STORAGE) || '0', 10);
            return Date.now() - t < POPUP_REPEAT_MS;
        } catch (e) { return false; }
    }

    function markPopupSeen() {
        try { localStorage.setItem(POPUP_STORAGE, String(Date.now())); } catch (e) { /* private mode */ }
    }

    function buildPopup() {
        var onPricingPage = /services\.html/.test(window.location.pathname);
        var wrap = document.createElement('div');
        wrap.className = 'promo-pop';
        wrap.setAttribute('role', 'dialog');
        wrap.setAttribute('aria-modal', 'true');
        wrap.setAttribute('aria-labelledby', 'promoPopTitle');
        wrap.hidden = true;
        wrap.innerHTML =
            '<div class="promo-pop__backdrop" data-promo-close></div>' +
            '<div class="promo-pop__card" tabindex="-1">' +
                '<button type="button" class="promo-pop__close" data-promo-close aria-label="Fermer l’offre">&times;</button>' +
                '<div class="promo-pop__visual">' +
                    '<span class="promo-pop__tag">' + LABEL + '</span>' +
                    '<p class="promo-pop__big">−' + Math.round(RATE * 100) + '%</p>' +
                '</div>' +
                '<div class="promo-pop__body">' +
                    '<h2 id="promoPopTitle" class="promo-pop__title">Sur toutes nos prestations</h2>' +
                    '<p class="promo-pop__text">Intérieur, extérieur ou pack complet : préparez votre voiture pour l’hiver, sans bouger de chez vous.</p>' +
                    '<p class="promo-pop__ends">L’offre se termine dans</p>' +
                    '<div class="cd" data-promo-countdown></div>' +
                    '<a class="promo-pop__cta" href="' + (onPricingPage ? '#car-showcase-container' : 'services.html') + '">J’en profite <i class="fa-solid fa-arrow-right"></i></a>' +
                    '<button type="button" class="promo-pop__later" data-promo-close>Non merci</button>' +
                    '<p class="promo-pop__legal">Valable sur toutes les réservations jusqu’au ' + endLabel + ' inclus.</p>' +
                '</div>' +
            '</div>';
        document.body.appendChild(wrap);

        var lastFocus = null;

        function close() {
            wrap.classList.remove('is-open');
            document.documentElement.classList.remove('promo-pop-open');
            document.removeEventListener('keydown', onKey);
            setTimeout(function () { wrap.hidden = true; }, 300);
            if (lastFocus && lastFocus.focus) lastFocus.focus();
        }

        function onKey(e) { if (e.key === 'Escape') { track('promo_popup_close'); close(); } }

        wrap.querySelectorAll('[data-promo-close]').forEach(function (el) {
            el.addEventListener('click', function () { track('promo_popup_close'); close(); });
        });
        wrap.querySelector('.promo-pop__cta').addEventListener('click', function () {
            track('promo_popup_cta');
            if (onPricingPage) close();
        });

        return function open() {
            lastFocus = document.activeElement;
            wrap.hidden = false;
            renderCountdowns();
            document.documentElement.classList.add('promo-pop-open');
            requestAnimationFrame(function () { wrap.classList.add('is-open'); });
            wrap.querySelector('.promo-pop__card').focus({ preventScroll: true });
            document.addEventListener('keydown', onKey);
            markPopupSeen();
            track('promo_popup_view');
        };
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Banner text, all derived from the constants above
        document.querySelectorAll('[data-promo-label]').forEach(function (el) { el.textContent = LABEL; });
        document.querySelectorAll('[data-promo-until]').forEach(function (el) { el.textContent = endLabel; });
        document.querySelectorAll('[data-promo-text]').forEach(function (el) {
            el.textContent = '−' + Math.round(RATE * 100) + '% sur toutes les prestations jusqu’au ' + endLabel;
        });
        var days = daysLeft();
        document.querySelectorAll('[data-promo-days]').forEach(function (el) {
            el.textContent = days <= 1 ? 'Dernier jour' : 'Plus que ' + days + ' jours';
        });

        // "À partir de 49€" → "À partir de 49€ 39€" (old price struck)
        document.querySelectorAll('[data-from-price]').forEach(function (el) {
            var p = parseInt(el.getAttribute('data-from-price'), 10);
            el.innerHTML = 'À partir de <s class="promo-old">' + euros(p) + '</s> ' + euros(apply(p));
        });

        // Option supplements "+20€" → "+20€ +16€"
        document.querySelectorAll('[data-option-price]').forEach(function (el) {
            var p = parseInt(el.getAttribute('data-option-price'), 10);
            el.innerHTML = '<s class="promo-old">+' + euros(p) + '</s> +' + euros(apply(p));
        });

        // Arrival popup (once a day at most)
        if (!popupRecentlySeen()) {
            var openPopup = buildPopup();
            // Never stack the offer on top of the cookie banner: wait for an answer first
            var openWhenFree = function () {
                var cookieBanner = document.querySelector('.cookie-banner');
                if (cookieBanner && !cookieBanner.hidden) {
                    cookieBanner.addEventListener('click', function retry(e) {
                        if (!e.target.closest('[data-cookie]')) return;
                        cookieBanner.removeEventListener('click', retry);
                        setTimeout(openPopup, 800);
                    });
                } else {
                    openPopup();
                }
            };
            setTimeout(openWhenFree, POPUP_DELAY_MS);
        }

        renderCountdowns();
        setInterval(renderCountdowns, 1000);
    });
})();
