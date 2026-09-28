/**
 * Continental Detailing — seasonal offer.
 * Single source of truth for the current promotion. Loaded in <head> (sync)
 * so the banner and prices are right on first paint. After END the offer
 * switches itself off everywhere: no code change needed on November 1st.
 */
(function () {
    'use strict';

    var LABEL = 'Offre Automne';
    var RATE  = 0.20;
    // 31 October 2026, 23:59:59 Paris time (CET, summer time ends 25 Oct)
    var END   = new Date('2026-10-31T23:59:59+01:00');

    var active = Date.now() <= END.getTime();

    function apply(value) {
        if (!active || typeof value !== 'number' || !value) return value;
        return Math.round(value * (1 - RATE));
    }

    function daysLeft() {
        return Math.max(0, Math.ceil((END.getTime() - Date.now()) / 86400000));
    }

    window.PROMO = {
        active: active,
        label: LABEL,
        rate: RATE,
        percent: Math.round(RATE * 100),
        end: END,
        apply: apply,
        daysLeft: daysLeft
    };

    if (!active) return;

    document.documentElement.classList.add('promo-on');

    function euros(v) { return v + '€'; }

    document.addEventListener('DOMContentLoaded', function () {
        // Banner text, all derived from the constants above
        var endLabel = END.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', timeZone: 'Europe/Paris' });
        document.querySelectorAll('[data-promo-label]').forEach(function (el) { el.textContent = LABEL; });
        document.querySelectorAll('[data-promo-text]').forEach(function (el) {
            el.textContent = '−' + Math.round(RATE * 100) + '% sur toutes les prestations jusqu’au ' + endLabel;
        });

        // Banner countdown
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
    });
})();
