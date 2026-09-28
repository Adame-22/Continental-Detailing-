/**
 * Continental Detailing — cookie consent (CNIL).
 * Google Analytics and Google Tag Manager are only loaded once the visitor
 * has clicked "Accepter". Refusing is as easy as accepting, the choice is
 * kept 6 months, and any [data-cookie-settings] link reopens the banner.
 * Loaded in <head> of every page.
 */
(function () {
    'use strict';

    var GA_ID  = 'G-K3PHWTTYR2';
    var GTM_ID = 'GTM-KRXZ2QSL';
    var STORAGE = 'cdCookieConsent';
    var MAX_AGE_MS = 182 * 24 * 60 * 60 * 1000; // ~6 months, then ask again

    // gtag() always exists so site code can call it; nothing is sent to
    // Google until the tags are actually loaded after consent.
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

    function readChoice() {
        try {
            var saved = JSON.parse(localStorage.getItem(STORAGE) || 'null');
            if (saved && (saved.v === 'granted' || saved.v === 'denied') && Date.now() - saved.t < MAX_AGE_MS) return saved.v;
        } catch (e) { /* private mode or bad value */ }
        return null;
    }

    function saveChoice(v) {
        try { localStorage.setItem(STORAGE, JSON.stringify({ v: v, t: Date.now() })); } catch (e) { /* private mode */ }
    }

    var loaded = false;
    function loadAnalytics() {
        if (loaded) return;
        loaded = true;
        gtag('js', new Date());
        gtag('config', GA_ID);
        var ga = document.createElement('script');
        ga.async = true;
        ga.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
        document.head.appendChild(ga);

        window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
        var gtm = document.createElement('script');
        gtm.async = true;
        gtm.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
        document.head.appendChild(gtm);
    }

    function clearGaCookies() {
        document.cookie.split(';').forEach(function (c) {
            var name = c.split('=')[0].trim();
            if (/^_ga/.test(name)) {
                var host = location.hostname.replace(/^www\./, '');
                ['', '; domain=' + host, '; domain=.' + host].forEach(function (d) {
                    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d;
                });
            }
        });
    }

    var choice = readChoice();
    if (choice === 'granted') loadAnalytics();

    var banner = null;
    function showBanner() {
        if (!banner) {
            banner = document.createElement('div');
            banner.className = 'cookie-banner';
            banner.setAttribute('role', 'region');
            banner.setAttribute('aria-label', 'Cookies');
            banner.innerHTML =
                '<p class="cookie-banner__text">Nous utilisons des cookies de mesure d’audience (Google Analytics) pour savoir comment le site est utilisé et l’améliorer. Aucun cookie publicitaire. ' +
                '<a href="/mentions-legales.html#cookies">En savoir plus</a></p>' +
                '<div class="cookie-banner__actions">' +
                    '<button type="button" class="cookie-banner__btn" data-cookie="denied">Refuser</button>' +
                    '<button type="button" class="cookie-banner__btn" data-cookie="granted">Accepter</button>' +
                '</div>';
            banner.querySelectorAll('[data-cookie]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var v = btn.getAttribute('data-cookie');
                    saveChoice(v);
                    if (v === 'granted') loadAnalytics();
                    else if (loaded) { clearGaCookies(); location.reload(); return; }
                    else clearGaCookies();
                    banner.hidden = true;
                });
            });
            document.body.appendChild(banner);
        }
        banner.hidden = false;
    }

    document.addEventListener('DOMContentLoaded', function () {
        if (!choice) showBanner();
        document.querySelectorAll('[data-cookie-settings]').forEach(function (el) {
            el.addEventListener('click', function (e) { e.preventDefault(); showBanner(); });
        });
    });
})();
