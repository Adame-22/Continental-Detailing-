#!/usr/bin/env python3
"""Génère les pages statiques qui partagent un même gabarit :
   - carte-cadeau.html, professionnels.html, contact.html
   - une page par ville (nettoyage-voiture-domicile-<ville>.html)

Les tarifs ci-dessous doivent rester identiques à ceux de services.html
(objet `tarifs` du simulateur). Après un changement de prix ou de texte :
    python3 tools/build_pages.py
puis commit des fichiers .html générés. Ce dossier n'est pas mis en ligne
(voir .vercelignore).
"""
import json
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://continentaldetailing.fr'

TARIFS = [  # (clé, nom, extérieur, intérieur, complet)
    ('citadine', 'Citadine', 49, 79, 119),
    ('berline', 'Berline', 59, 89, 129),
    ('suv', 'SUV', 69, 99, 139),
    ('mono5', 'Monospace 5 places', 79, 109, 149),
    ('mono7', 'Monospace 7 places', 89, 119, 159),
    ('prestige', 'Prestige / Sport', 89, 129, 199),
    ('moto', 'Moto', 39, 69, 99),
]


def wa(message):
    return 'https://wa.me/33750875964?text=' + urllib.parse.quote(message)


WA_INFO = wa('Bonjour, je souhaite un renseignement pour le nettoyage de ma voiture 🚗')

HEAD = '''<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
    <script>document.documentElement.classList.add('js');setTimeout(function(){if(!window.__motionReady)document.documentElement.classList.remove('js')},4000);</script>
    <script src="js/promo.js"></script>
    <!-- Mesure d'audience : chargée seulement après accord (bannière cookies) -->
    <script src="js/consent.js"></script>
    <!-- Statistiques de visite sans cookie (Vercel Web Analytics) -->
    <script>window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };</script>
    <script defer src="/_vercel/insights/script.js"></script>
    <link rel="icon" type="image/png" sizes="192x192" href="images/favicon.png">
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="canonical" href="{{canonical}}">
    <title>{{title}}</title>
    <meta name="description" content="{{description}}">
    <meta property="og:title" content="{{title}}">
    <meta property="og:description" content="{{description}}">
    <meta property="og:image" content="https://continentaldetailing.fr/images/hero-bg-hq.webp">
    <meta property="og:url" content="{{canonical}}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Continental Detailing">
    <meta property="og:locale" content="fr_FR">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com/">
    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/pages.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        bg: '#FFFFFF',
                        'bg-alt': '#F8F7F4',
                        'bg-dark': '#0E1418',
                        primary: '#1A1A1E',
                        secondary: '#5A5650',
                        muted: '#707070',
                        action: '#1A1A1E',
                        'action-lt': '#404040',
                    },
                    fontFamily: {
                        sans:  ['Outfit', 'sans-serif'],
                        serif: ['Outfit', 'sans-serif']
                    }
                }
            }
        }
    </script>
{{head_extra}}</head>
<body class="bg-bg text-primary font-sans antialiased">

    <!-- Bandeau saisonnier (réglages dans js/promo.js) -->
    <a href="services.html" class="promo-bar">
        <span class="promo-bar__tag" data-promo-label></span>
        <span class="promo-bar__text" data-promo-text></span>
        <span class="promo-bar__days" data-promo-days></span>
        <span class="promo-bar__cta">Réserver <i class="fa-solid fa-arrow-right"></i></span>
    </a>

    <nav class="nav-main" id="navbar">
        <div class="nav-inner">
            <a href="index.html" class="logo-link flex items-center">
                <img src="images/logo_continental.webp" alt="Continental Detailing" class="main-logo" style="height:44px; width:auto; object-fit:contain;">
            </a>
            <div class="nav-links">
                <a href="index.html" class="nav-link">Accueil</a>
                <a href="services.html" class="nav-link">Tarifs & Réservation</a>
                <a href="carte-cadeau.html" class="nav-link">Carte cadeau</a>
                <a href="professionnels.html" class="nav-link">Professionnels</a>
            </div>
            <a href="services.html" class="nav-mobile-cta">Tarifs <i class="fa-solid fa-arrow-right"></i></a>
        </div>
    </nav>
'''

FOOT = '''
    <footer class="footer mt-auto">
        <div class="footer-inner">
            <div class="footer-grid">
                <div>
                    <a href="index.html" class="logo-link flex items-center" style="margin-bottom: 24px;">
                        <img src="images/logo_continental_white.webp" alt="Continental Detailing" class="main-logo" style="height:44px; width:auto; object-fit:contain;">
                    </a>
                    <p class="text-sm font-light text-[rgba(255,255,255,0.5)] max-w-sm">
                        L'art du détail pour votre automobile. Detailing premium à domicile en Essonne et Seine-et-Marne.
                    </p>
                </div>
                <div>
                    <div class="footer-title">Navigation</div>
                    <a href="index.html" class="footer-link">Accueil</a>
                    <a href="about.html" class="footer-link">Qui sommes-nous</a>
                    <a href="services.html" class="footer-link">Tarifs & Réservation</a>
                    <a href="carte-cadeau.html" class="footer-link">Carte cadeau</a>
                    <a href="professionnels.html" class="footer-link">Professionnels</a>
                    <a href="avis.html" class="footer-link">Avis clients</a>
                    <a href="contact.html" class="footer-link">Contact</a>
                </div>
                <div>
                    <div class="footer-title">Contact</div>
                    <a href="mailto:continental.detailing.idf@gmail.com" class="footer-link">continental.detailing.idf@gmail.com</a>
                    <a href="''' + WA_INFO + '''" class="footer-link">WhatsApp ou SMS (+33 7 50 87 59 64) · réponse rapide</a>
                </div>
            </div>

            <div class="footer-bottom">
                <div class="footer-copy">© <span class="cd-year">2026</span> Continental Detailing — Tous droits réservés. &nbsp;·&nbsp;<a href="mentions-legales.html" style="color:#A0A0A0; text-decoration:underline;">Mentions légales</a>&nbsp;·&nbsp;<a href="mentions-legales.html#cookies" data-cookie-settings style="color:#A0A0A0; text-decoration:underline;">Cookies</a> &nbsp;·&nbsp;<a href="cgv.html" style="color:#A0A0A0; text-decoration:underline;">CGV</a></div>
                <div class="footer-socials">
                    <a href="mailto:continental.detailing.idf@gmail.com" aria-label="E-mail"><i class="fa-regular fa-envelope"></i></a>
                    <a href="https://www.instagram.com/continental.detailing.idf/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
                </div>
            </div>
        </div>
    </footer>

    <script src="js/motion.js"></script>
    <script>document.querySelectorAll(".cd-year").forEach(e=>e.textContent=new Date().getFullYear());</script>
</body>
</html>
'''


def render(template, **values):
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', value)
    assert '{{' not in template, template[template.index('{{'):][:60]
    return template


def write(name, html):
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
        f.write(html)
    print('écrit', name)


def jsonld(data):
    return '    <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'


def faq_block(faqs):
    items = ''.join(
        '''
                <details class="pg-faq">
                    <summary>''' + q + '''</summary>
                    <p>''' + a + '''</p>
                </details>''' for q, a in faqs)
    return '<div class="pg-faqs">' + items + '\n            </div>'


def faq_schema(faqs):
    return {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs],
    }


def tarif_rows():
    return ''.join(
        '''
                        <tr><th scope="row">''' + nom + '''</th><td>''' + str(ext) + '''€</td><td>''' + str(inte) + '''€</td><td class="pg-strong">''' + str(comp) + '''€</td></tr>'''
        for _, nom, ext, inte, comp in TARIFS)


# ───────────────────────── Pages par ville ─────────────────────────

VILLES = [
    {
        'slug': 'melun', 'nom': 'Melun', 'a': 'à Melun', 'cp': '77000', 'dept': 'Seine-et-Marne (77)',
        'intro': "Préfecture de la Seine-et-Marne, Melun est une ville où la voiture reste indispensable : trajets vers Paris par l'A5 ou la Francilienne, école, courses, week-ends. À ce rythme, l'habitacle s'encrasse vite et la carrosserie ternit sans qu'on trouve le temps de s'en occuper.",
        'intro2': "Continental Detailing se déplace chez vous, à Melun et dans les communes voisines, avec tout le matériel professionnel. Vous ne perdez pas une demi-journée dans une station de lavage : nous venons le week-end ou en soirée, et vous restez chez vous pendant que votre voiture retrouve son éclat.",
        'angle_titre': 'Pensé pour ceux qui roulent tous les jours',
        'angle': "Miettes, traces de café, poussière dans les aérations, tapis gorgés de saleté : c'est le quotidien des voitures qui font la navette. Notre formule Intérieur traite tout cela en profondeur — aspiration jusque dans les rails de sièges, shampoing des tissus par injection-extraction, plastiques nettoyés au pinceau et vitres sans trace.",
        'voisines': ['Dammarie-les-Lys', 'Le Mée-sur-Seine', 'Vaux-le-Pénil', 'La Rochette', 'Rubelles', 'Maincy', 'Livry-sur-Seine'],
        'faq': ("Mes sièges en tissu sont tachés, pouvez-vous les rattraper ?",
                "Dans la plupart des cas, oui. La formule Intérieur comprend un shampoing des fibres par injection-extraction, bien plus efficace qu'un simple aspirateur. Le résultat dépend de l'ancienneté et de la nature des taches : nous vous donnons un avis honnête avant de commencer."),
    },
    {
        'slug': 'evry-courcouronnes', 'nom': 'Évry-Courcouronnes', 'a': 'à Évry-Courcouronnes', 'cp': '91000', 'dept': 'Essonne (91)',
        'intro': "À Évry-Courcouronnes, préfecture de l'Essonne, beaucoup d'automobilistes vivent en résidence ou en appartement et n'ont ni le temps ni l'équipement pour entretenir correctement leur véhicule. Les rouleaux des stations rayent la peinture, et le nettoyage intérieur y est expédié.",
        'intro2': "Continental Detailing vient directement à vous : devant votre domicile, sur le parking de votre résidence ou sur votre lieu de travail. Nous apportons le matériel, les produits et le savoir-faire d'un atelier de detailing, sans que vous ayez à vous déplacer.",
        'angle_titre': 'En appartement ou en résidence ? C’est possible',
        'angle': "Il nous faut simplement une prise électrique standard et un point d'eau à proximité du véhicule : parking de résidence équipé, garage, domicile d'un proche ou parking de votre entreprise. Nous fournissons rallonges et tuyaux. En cas de doute, envoyez-nous une photo de l'emplacement par message, nous vous disons tout de suite si c'est faisable.",
        'voisines': ['Ris-Orangis', 'Lisses', 'Bondoufle', 'Grigny', 'Soisy-sur-Seine', 'Étiolles', 'Corbeil-Essonnes'],
        'faq': ("Je n'ai pas de place de parking privée, comment faire ?",
                "Le plus simple est de choisir un endroit où le véhicule peut stationner quelques heures avec un accès à l'eau et à une prise : parking de résidence, chez un proche ou sur votre lieu de travail avec l'accord de l'employeur. Décrivez-nous votre situation par message, nous trouvons une solution ensemble."),
    },
    {
        'slug': 'fontainebleau', 'nom': 'Fontainebleau', 'a': 'à Fontainebleau', 'cp': '77300', 'dept': 'Seine-et-Marne (77)',
        'intro': "Vivre à Fontainebleau, c'est profiter de la forêt… et la retrouver dans sa voiture. Sable, boue, aiguilles de pin dans les tapis, sève et résine sur la carrosserie quand on stationne sous les arbres : autant de salissures qui s'incrustent et abîment les surfaces si on les laisse.",
        'intro2': "Continental Detailing intervient à domicile à Fontainebleau, à Avon et dans les villages alentour. Nous utilisons des méthodes douces — prélavage à la mousse active, lavage aux deux seaux, produits pH neutre — adaptées aussi bien à la voiture de tous les jours qu'aux véhicules de prestige.",
        'angle_titre': 'Après la forêt, un vrai nettoyage',
        'angle': "Le sable et la terre agissent comme un abrasif : frottés à l'éponge ou aux rouleaux, ils rayent le vernis. Notre formule Extérieur commence par un prélavage sans contact qui décolle les salissures avant tout passage du gant, puis traite jantes, joints et logos au pinceau. À l'intérieur, l'aspiration va chercher le sable jusque dans les rails de sièges et le coffre.",
        'voisines': ['Avon', 'Samois-sur-Seine', 'Bois-le-Roi', 'Thomery', 'Vulaines-sur-Seine', 'Héricy', 'Bourron-Marlotte'],
        'faq': ("Vous occupez-vous des voitures de sport et de collection ?",
                "Oui. Nous avons une catégorie Prestige / Sport, avec la même méthode sécurisée : prélavage sans contact, lavage aux deux seaux, microfibres haute densité et produits pH neutre. Pour un véhicule de collection ou une demande particulière, contactez-nous d'abord par message pour en parler."),
    },
    {
        'slug': 'corbeil-essonnes', 'nom': 'Corbeil-Essonnes', 'a': 'à Corbeil-Essonnes', 'cp': '91100', 'dept': 'Essonne (91)',
        'intro': "À Corbeil-Essonnes, au confluent de la Seine et de l'Essonne, la voiture sert à tout : travail, enfants, courses, départs en week-end. Entre deux lavages rapides, la saleté s'installe dans les tissus, les plastiques ternissent et la peinture perd son éclat.",
        'intro2': "Continental Detailing se déplace à votre adresse, à Corbeil-Essonnes comme dans les communes voisines, pour un nettoyage complet réalisé à la main. Vous choisissez la formule, nous venons avec tout l'équipement.",
        'angle_titre': 'Vous vendez votre voiture ? Préparez-la',
        'angle': "Une voiture propre se photographie mieux, se vend plus vite et se négocie moins. Avant de publier votre annonce, un Pack Complet remet l'habitacle et la carrosserie en valeur : sièges et tapis shampouinés, plastiques rénovés, jantes décontaminées, vitres impeccables. C'est souvent l'investissement le plus rentable avant une vente.",
        'voisines': ['Saint-Germain-lès-Corbeil', 'Villabé', 'Saintry-sur-Seine', 'Le Coudray-Montceaux', 'Saint-Pierre-du-Perray', 'Ormoy', 'Étiolles'],
        'faq': ("Quelle formule choisir avant de vendre ma voiture ?",
                "Le Pack Complet est le plus adapté : il traite à la fois l'intérieur et l'extérieur, ce que regarde un acheteur. Si la carrosserie est déjà propre, la formule Intérieur seule suffit souvent à transformer les photos de l'annonce."),
    },
    {
        'slug': 'savigny-le-temple', 'nom': 'Savigny-le-Temple', 'a': 'à Savigny-le-Temple', 'cp': '77176', 'dept': 'Seine-et-Marne (77)',
        'intro': "À Savigny-le-Temple et dans tout le secteur de Sénart, la voiture familiale ne chôme pas : trajets d'école, activités, courses au Carré Sénart, vacances. Miettes dans les sièges auto, taches sur la banquette, poils du chien dans le coffre… l'intérieur en prend un coup.",
        'intro2': "Continental Detailing vient chez vous, dans votre allée ou devant votre pavillon, avec tout le matériel. Pendant que nous nous occupons de la voiture, vous continuez votre journée à la maison.",
        'angle_titre': 'La voiture des familles, remise à neuf',
        'angle': "Monospaces, SUV et breaks sont notre quotidien. Nous déposons les tapis pour les shampouiner, aspirons sous et entre les sièges, nettoyons les plastiques au pinceau et traitons les tissus par injection-extraction. Poils d'animaux ou véhicule très chargé : dites-le-nous à la réservation, nous prévoyons le temps nécessaire (un supplément peut s'appliquer, il est affiché dans le simulateur).",
        'voisines': ['Cesson', 'Nandy', 'Lieusaint', 'Moissy-Cramayel', 'Vert-Saint-Denis', 'Réau', 'Combs-la-Ville'],
        'faq': ("Faut-il retirer les sièges auto avant votre passage ?",
                "C'est préférable : cela nous permet de nettoyer correctement la banquette en dessous, là où les miettes s'accumulent. Pensez aussi à vider le coffre et les vide-poches ; un véhicule non vidé fait l'objet d'un petit supplément indiqué dans le simulateur."),
    },
    {
        'slug': 'massy', 'nom': 'Massy', 'a': 'à Massy', 'cp': '91300', 'dept': 'Essonne (91)',
        'intro': "À Massy, entre la gare TGV, les RER et le quartier d'affaires Atlantis, les journées sont chargées et le temps manque pour s'occuper de sa voiture. Résultat : on repousse le nettoyage de semaine en semaine.",
        'intro2': "Continental Detailing vous fait gagner ce temps. Nous intervenons chez vous, à Massy et dans les communes voisines, le samedi, le dimanche ou en semaine après 19h : pas de demi-journée à poser, pas de file d'attente en station.",
        'angle_titre': 'Le week-end ou après le travail',
        'angle': "Vous rentrez tard ? Nous venons en semaine à partir de 19h, ou le samedi et le dimanche en journée. Il nous faut simplement une prise électrique et un point d'eau à proximité du véhicule. Vous êtes dirigeant ou gestionnaire de flotte ? Nous entretenons aussi les véhicules de société le samedi, quand ils sont à l'arrêt, sur devis.",
        'voisines': ['Palaiseau', 'Verrières-le-Buisson', 'Igny', 'Chilly-Mazarin', 'Wissous', 'Champlan', 'Longjumeau'],
        'faq': ("Pouvez-vous intervenir sur le parking de mon entreprise ?",
                "Oui, le samedi ou en soirée, si l'employeur ou le gestionnaire du parking est d'accord et qu'une prise électrique standard et un point d'eau sont accessibles près du véhicule. Nous apportons rallonges et tuyaux. Pour plusieurs véhicules, consultez notre page Professionnels."),
    },
]

CITY_BODY = '''
    <main>
        <section class="pg-hero">
            <div class="pg-wrap">
                <nav class="pg-crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a><span>›</span><a href="index.html#zone">Zone d'intervention</a><span>›</span>{{nom}}</nav>
                <p class="pg-eyebrow">{{dept}} · {{cp}}</p>
                <h1 class="pg-h1">Nettoyage voiture à domicile {{a}}</h1>
                <p class="pg-lead">Detailing premium intérieur et extérieur, réalisé à la main chez vous ou sur votre lieu de travail. Extérieur dès 49€, intérieur dès 79€, pack complet dès 119€.</p>
                <div class="pg-actions">
                    <a href="services.html" class="pg-btn pg-btn--dark">Calculer mon prix <i class="fa-solid fa-arrow-right"></i></a>
                    <a href="{{wa}}" target="_blank" rel="noopener noreferrer" class="pg-btn pg-btn--line"><i class="fa-brands fa-whatsapp"></i> Écrire sur WhatsApp</a>
                </div>
                <ul class="pg-chips">
                    <li><i class="fa-solid fa-house"></i> À domicile ou au travail</li>
                    <li><i class="fa-solid fa-droplet"></i> Produits pH neutre</li>
                    <li><i class="fa-solid fa-hand-sparkles"></i> Lavage à la main, méthode 2 seaux</li>
                </ul>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap pg-two">
                <div class="pg-prose reveal">
                    <h2 class="pg-h2">Votre voiture nettoyée {{a}}, sans vous déplacer</h2>
                    <p>{{intro}}</p>
                    <p>{{intro2}}</p>
                </div>
                <aside class="pg-card pg-card--tint reveal stagger-1">
                    <h3 class="pg-h3">{{angle_titre}}</h3>
                    <p>{{angle}}</p>
                </aside>
            </div>
        </section>

        <section class="pg-section pg-section--alt">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Tarifs du nettoyage auto {{a}}</h2>
                <p class="pg-sub reveal">Les mêmes prix partout dans notre zone d'intervention. Le tarif exact dépend du gabarit et de l'état du véhicule ; il vous est confirmé avant l'intervention.</p>
                <div class="pg-table-wrap reveal">
                    <table class="pg-table">
                        <thead><tr><th scope="col">Véhicule</th><th scope="col">Extérieur</th><th scope="col">Intérieur</th><th scope="col">Pack Complet</th></tr></thead>
                        <tbody>{{tarifs}}
                        </tbody>
                    </table>
                </div>
                <p class="pg-note">Utilitaire : sur devis. Options (cire, poils d'animaux…) et prix détaillé dans le <a href="services.html">simulateur en ligne</a>.</p>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Comment ça se passe ?</h2>
                <ol class="pg-steps">
                    <li class="reveal"><span>1</span><h3>Vous estimez votre prix</h3><p>Choisissez votre véhicule et votre formule dans le simulateur : le tarif s'affiche tout de suite.</p></li>
                    <li class="reveal stagger-1"><span>2</span><h3>On fixe un créneau</h3><p>Le samedi ou le dimanche en journée, ou en semaine après 19h. Un acompte de 40€, déduit du total, bloque votre date.</p></li>
                    <li class="reveal stagger-2"><span>3</span><h3>On vient {{a}}</h3><p>Avec tout le matériel. Il nous faut seulement une prise électrique et un point d'eau à proximité.</p></li>
                    <li class="reveal stagger-3"><span>4</span><h3>Vous retrouvez une voiture propre</h3><p>Comptez 2 à 3 heures pour un intérieur ou un extérieur, 4 à 5 heures pour un pack complet.</p></li>
                </ol>
            </div>
        </section>

        <section class="pg-section pg-section--alt">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Autour de {{nom}}</h2>
                <p class="pg-sub reveal">Nous intervenons {{a}} et dans les communes voisines :</p>
                <ul class="pg-tags reveal">{{voisines}}</ul>
                <p class="pg-note">Votre commune n'est pas dans la liste ? <a href="{{wa}}" target="_blank" rel="noopener noreferrer">Écrivez-nous</a>, nous couvrons une grande partie de l'Essonne et de la Seine-et-Marne.</p>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap pg-narrow">
                <h2 class="pg-h2 reveal">Questions fréquentes</h2>
                {{faq}}
            </div>
        </section>

        <section class="pg-cta">
            <div class="pg-wrap pg-narrow">
                <h2>Prêt à redonner de l'éclat à votre voiture ?</h2>
                <p>Obtenez votre prix en deux minutes, puis réservez par message.</p>
                <div class="pg-actions pg-actions--center">
                    <a href="services.html" class="pg-btn pg-btn--light">Calculer mon prix <i class="fa-solid fa-arrow-right"></i></a>
                    <a href="carte-cadeau.html" class="pg-btn pg-btn--ghost"><i class="fa-solid fa-gift"></i> Offrir une carte cadeau</a>
                </div>
                <p class="pg-also">Nous intervenons aussi à : {{autres}}</p>
            </div>
        </section>
    </main>
'''


def build_villes():
    for v in VILLES:
        nom, a = v['nom'], v['a']
        faqs = [
            ('Combien coûte un nettoyage de voiture à domicile ' + a + ' ?',
             "Pour une citadine : 49€ en extérieur, 79€ en intérieur et 119€ en pack complet. Le prix varie selon le gabarit du véhicule (berline, SUV, monospace…) et son état. Le simulateur en ligne vous donne votre tarif en deux minutes."),
            ('De quoi avez-vous besoin sur place ?',
             "D'une prise électrique standard et d'un point d'eau à proximité du véhicule. Nous apportons tout le reste : matériel, produits, rallonges et tuyaux."),
            v['faq'],
            ('Combien de temps dure la prestation ?',
             "Comptez 2 à 3 heures pour un nettoyage intérieur ou extérieur, et 4 à 5 heures pour un pack complet. La durée dépend de la taille et de l'état du véhicule."),
            ('Quand intervenez-vous ' + a + ' ?',
             "Le samedi et le dimanche en journée, et en semaine à partir de 19h. Pensez à réserver votre samedi quelques jours à l'avance."),
            ('Comment réserver ' + a + ' ?',
             "Estimez votre prix dans le simulateur, puis écrivez-nous par WhatsApp, SMS ou Instagram pour choisir un créneau. Un acompte de 40€, déduit du total, valide le rendez-vous ; le solde se règle après la prestation."),
        ]
        url = SITE + '/nettoyage-voiture-domicile-' + v['slug'] + '.html'
        schemas = jsonld({
            '@context': 'https://schema.org', '@type': 'Service',
            'name': 'Nettoyage voiture à domicile ' + a,
            'serviceType': 'Nettoyage et detailing automobile à domicile',
            'provider': {'@id': SITE + '/#localbusiness'},
            'areaServed': {'@type': 'City', 'name': nom},
            'url': url,
            'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'EUR', 'lowPrice': '39', 'highPrice': '199'},
        }) + jsonld(faq_schema(faqs)) + jsonld({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Nettoyage voiture à domicile ' + a, 'item': url},
            ]})
        autres = ', '.join('<a href="nettoyage-voiture-domicile-' + o['slug'] + '.html">' + o['nom'] + '</a>'
                           for o in VILLES if o is not v)
        head = render(HEAD, canonical=url,
                      title='Nettoyage voiture à domicile ' + a + ' (' + v['cp'] + ') — dès 49€ | Continental Detailing',
                      description='Nettoyage et detailing auto à domicile ' + a + ' : intérieur, extérieur ou pack complet, réalisé à la main chez vous. Extérieur dès 49€. Devis en 2 minutes, réservation par message.',
                      head_extra=schemas)
        body = render(CITY_BODY, nom=nom, a=a, cp=v['cp'], dept=v['dept'],
                      intro=v['intro'], intro2=v['intro2'], angle_titre=v['angle_titre'], angle=v['angle'],
                      tarifs=tarif_rows(), faq=faq_block(faqs), autres=autres,
                      voisines=''.join('<li>' + c + '</li>' for c in [nom] + v['voisines']),
                      wa=wa('Bonjour, je souhaite un nettoyage de voiture à domicile ' + a + ' 🚗'))
        write('nettoyage-voiture-domicile-' + v['slug'] + '.html', head + body + FOOT)


# ───────────────────────── Professionnels ─────────────────────────

PRO_FAQS = [
    ("Comment est établi le prix pour une entreprise ?",
     "Sur devis, selon le nombre de véhicules, leur gabarit, leur état et la fréquence souhaitée. Le devis est gratuit et sans engagement."),
    ("Fournissez-vous une facture ?",
     "Oui, une facture est émise pour chaque intervention ou regroupée en fin de mois selon ce qui vous arrange. TVA non applicable, article 293 B du CGI."),
    ("Où a lieu l'intervention ?",
     "Sur votre site : parking de l'entreprise, dépôt, agence ou concession. Il nous faut une prise électrique standard et un point d'eau à proximité des véhicules ; nous apportons le reste."),
    ("Quand intervenez-vous ?",
     "Le samedi et le dimanche en journée, et en semaine à partir de 19h. Vos véhicules ne sont donc jamais immobilisés pendant vos heures de travail."),
    ("Pouvez-vous passer régulièrement ?",
     "Oui. Nous pouvons convenir d'un passage régulier, par exemple un samedi par mois ou un samedi sur deux, pour que vos véhicules restent présentables toute l'année."),
]

PRO_BODY = '''
    <main>
        <section class="pg-hero">
            <div class="pg-wrap">
                <p class="pg-eyebrow">Professionnels · Essonne & Seine-et-Marne</p>
                <h1 class="pg-h1">L'entretien de vos véhicules, sur votre site</h1>
                <p class="pg-lead">Flottes d'entreprise, utilitaires, véhicules d'occasion à préparer : nous nettoyons vos véhicules sur votre parking le samedi, quand ils sont à l'arrêt, ou en soirée. Aucune immobilisation pendant vos heures de travail.</p>
                <div class="pg-actions">
                    <a href="{{wa}}" target="_blank" rel="noopener noreferrer" class="pg-btn pg-btn--dark"><i class="fa-brands fa-whatsapp"></i> Demander un devis</a>
                    <a href="{{mail}}" class="pg-btn pg-btn--line"><i class="fa-regular fa-envelope"></i> Par e-mail</a>
                </div>
                <ul class="pg-chips">
                    <li><i class="fa-solid fa-file-invoice"></i> Devis gratuit, facture fournie</li>
                    <li><i class="fa-solid fa-calendar-check"></i> Le samedi ou en soirée</li>
                    <li><i class="fa-solid fa-location-dot"></i> Intervention sur site</li>
                </ul>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Pour qui ?</h2>
                <div class="pg-grid3">
                    <div class="pg-card reveal"><i class="fa-solid fa-building pg-icon"></i><h3 class="pg-h3">Entreprises & flottes</h3><p>Véhicules de fonction et de service entretenus sur votre parking le samedi ou en soirée, quand ils ne roulent pas. Une image soignée chez vos clients.</p></div>
                    <div class="pg-card reveal stagger-1"><i class="fa-solid fa-truck pg-icon"></i><h3 class="pg-h3">Artisans & utilitaires</h3><p>Cabine dépoussiérée, sièges shampouinés, carrosserie propre : votre utilitaire est votre première carte de visite.</p></div>
                    <div class="pg-card reveal stagger-2"><i class="fa-solid fa-car-side pg-icon"></i><h3 class="pg-h3">Garages & vendeurs VO</h3><p>Préparation esthétique avant mise en vente : un véhicule impeccable se photographie mieux et part plus vite.</p></div>
                    <div class="pg-card reveal"><i class="fa-solid fa-taxi pg-icon"></i><h3 class="pg-h3">VTC, taxis & auto-écoles</h3><p>Un habitacle propre et sans odeur, c'est ce que remarquent vos clients en premier. Entretien régulier à jour fixe.</p></div>
                    <div class="pg-card reveal stagger-1"><i class="fa-solid fa-key pg-icon"></i><h3 class="pg-h3">Loueurs & conciergeries</h3><p>Remise en état entre deux locations, directement là où le véhicule est stationné.</p></div>
                    <div class="pg-card reveal stagger-2"><i class="fa-solid fa-handshake pg-icon"></i><h3 class="pg-h3">Agences & commerciaux</h3><p>Les véhicules de vos commerciaux reflètent votre enseigne : nous les gardons présentables toute l'année.</p></div>
                </div>
            </div>
        </section>

        <section class="pg-section pg-section--alt">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Comment ça marche ?</h2>
                <ol class="pg-steps">
                    <li class="reveal"><span>1</span><h3>Vous décrivez votre besoin</h3><p>Nombre de véhicules, type, ville et fréquence souhaitée, par message ou par e-mail.</p></li>
                    <li class="reveal stagger-1"><span>2</span><h3>Vous recevez un devis</h3><p>Gratuit et sans engagement, adapté à votre volume et à vos contraintes.</p></li>
                    <li class="reveal stagger-2"><span>3</span><h3>Nous intervenons sur site</h3><p>Le samedi, le dimanche ou en soirée, avec tout le matériel. Prise électrique et point d'eau requis.</p></li>
                    <li class="reveal stagger-3"><span>4</span><h3>Vous recevez la facture</h3><p>À chaque passage ou en fin de mois. Paiement par virement.</p></li>
                </ol>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap pg-narrow">
                <h2 class="pg-h2 reveal">Questions fréquentes</h2>
                {{faq}}
            </div>
        </section>

        <section class="pg-cta">
            <div class="pg-wrap pg-narrow">
                <h2>Parlons de vos véhicules</h2>
                <p>Indiquez-nous le nombre de véhicules et votre ville : nous revenons vers vous avec un devis.</p>
                <div class="pg-actions pg-actions--center">
                    <a href="{{wa}}" target="_blank" rel="noopener noreferrer" class="pg-btn pg-btn--light"><i class="fa-brands fa-whatsapp"></i> Demander un devis</a>
                    <a href="{{mail}}" class="pg-btn pg-btn--ghost"><i class="fa-regular fa-envelope"></i> continental.detailing.idf@gmail.com</a>
                </div>
            </div>
        </section>
    </main>
'''


def build_pro():
    url = SITE + '/professionnels.html'
    message = ("Bonjour, je souhaite un devis pour l'entretien des véhicules de mon entreprise.\n"
               "Société : \nNombre et type de véhicules : \nVille : \nFréquence souhaitée : ")
    mail = ('mailto:continental.detailing.idf@gmail.com?subject=' + urllib.parse.quote('Demande de devis professionnel')
            + '&body=' + urllib.parse.quote(message))
    head = render(HEAD, canonical=url,
                  title='Nettoyage de véhicules pour professionnels — flottes, utilitaires, garages | Continental Detailing',
                  description="Entretien et nettoyage de véhicules d'entreprise sur site en Essonne (91) et Seine-et-Marne (77) : flottes, utilitaires, préparation de véhicules d'occasion. Devis gratuit, facture fournie.",
                  head_extra=jsonld(faq_schema(PRO_FAQS)))
    write('professionnels.html', head + render(PRO_BODY, wa=wa(message), mail=mail, faq=faq_block(PRO_FAQS)) + FOOT)


# ───────────────────────── Carte cadeau ─────────────────────────

GIFT_FAQS = [
    ("Comment est envoyée la carte cadeau ?",
     "Au format numérique (PDF), par WhatsApp ou par e-mail, à vous ou directement à la personne de votre choix. Vous pouvez l'imprimer pour l'offrir en main propre."),
    ("Combien de temps la carte est-elle valable ?",
     "12 mois à compter de la date d'achat. La date limite est indiquée sur la carte."),
    ("Et si la voiture du bénéficiaire est plus grande que prévu ?",
     "Aucun problème : la valeur de la carte est déduite du prix de la prestation réellement réalisée, et le bénéficiaire règle simplement la différence. S'il choisit une prestation moins chère, il peut ajouter une option."),
    ("Où le bénéficiaire peut-il utiliser sa carte ?",
     "Partout dans notre zone d'intervention, en Essonne (91) et en Seine-et-Marne (77). Il réserve par message en indiquant le code de la carte, et nous venons chez lui."),
    ("Comment payer ?",
     "Par Wero (Paylib) ou par virement instantané, sans frais. Les coordonnées vous sont communiquées dès réception de votre commande, et la carte est envoyée une fois le paiement reçu."),
]

GIFT_BODY = '''
    <main x-data="carteCadeau()">
        <section class="pg-hero">
            <div class="pg-wrap pg-two pg-two--center">
                <div>
                    <p class="pg-eyebrow"><span data-noel hidden>Idée cadeau de Noël · </span>Carte cadeau</p>
                    <h1 class="pg-h1">Offrez une voiture comme neuve</h1>
                    <p class="pg-lead">Un cadeau utile, qui fait vraiment plaisir : un nettoyage premium réalisé à domicile, chez la personne de votre choix. Elle n'a rien à faire, nous venons à elle.</p>
                    <ul class="pg-chips">
                        <li><i class="fa-solid fa-paper-plane"></i> Envoyée par WhatsApp ou e-mail</li>
                        <li><i class="fa-solid fa-calendar"></i> Valable 12 mois</li>
                        <li><i class="fa-solid fa-location-dot"></i> Essonne & Seine-et-Marne</li>
                    </ul>
                </div>
                <div class="gift-card" aria-hidden="true">
                    <img src="images/logo_continental_white.webp" alt="" class="gift-card__logo">
                    <p class="gift-card__label">Carte cadeau</p>
                    <p class="gift-card__offer" x-text="libelle"></p>
                    <p class="gift-card__value" x-text="prix + '€'"></p>
                    <p class="gift-card__names"><span x-text="pour ? 'Pour ' + pour : 'Pour la personne de votre choix'"></span><span x-show="de" x-text="' · De la part de ' + de"></span></p>
                </div>
            </div>
        </section>

        <section class="pg-section" id="composer">
            <div class="pg-wrap pg-narrow">
                <h2 class="pg-h2">Composez votre carte</h2>

                <div class="gift-tabs" role="tablist">
                    <button type="button" role="tab" :aria-selected="mode === 'formule'" :class="mode === 'formule' && 'is-on'" @click="mode = 'formule'">Une prestation</button>
                    <button type="button" role="tab" :aria-selected="mode === 'montant'" :class="mode === 'montant' && 'is-on'" @click="mode = 'montant'">Un montant libre</button>
                </div>

                <div x-show="mode === 'formule'">
                    <p class="gift-step">1. Le véhicule du bénéficiaire</p>
                    <div class="gift-options">
                        <template x-for="v in vehicules" :key="v.id">
                            <button type="button" class="gift-opt" :class="vehicule === v.id && 'is-on'" :aria-pressed="vehicule === v.id" @click="vehicule = v.id" x-text="v.nom"></button>
                        </template>
                    </div>
                    <p class="pg-note">Vous ne savez pas ? Choisissez « Un montant libre » : la valeur sera déduite de la prestation.</p>

                    <p class="gift-step">2. La formule</p>
                    <div class="gift-options gift-options--3">
                        <template x-for="f in formules" :key="f.id">
                            <button type="button" class="gift-opt gift-opt--big" :class="formule === f.id && 'is-on'" :aria-pressed="formule === f.id" @click="formule = f.id">
                                <strong x-text="f.nom"></strong>
                                <small x-text="f.detail"></small>
                                <b><s class="promo-old" x-show="promoOn" x-text="tarifNormal(f.id) + '€'"></s> <span x-text="tarif(f.id) + '€'"></span></b>
                            </button>
                        </template>
                    </div>
                </div>

                <div x-show="mode === 'montant'">
                    <p class="gift-step">Montant de la carte</p>
                    <div class="gift-options">
                        <template x-for="m in montants" :key="m">
                            <button type="button" class="gift-opt" :class="montant === m && 'is-on'" :aria-pressed="montant === m" @click="montant = m" x-text="m + '€'"></button>
                        </template>
                    </div>
                    <p class="pg-note">Le montant est déduit du prix de la prestation choisie par le bénéficiaire.</p>
                </div>

                <p class="gift-step" x-text="mode === 'formule' ? '3. Personnalisez (facultatif)' : 'Personnalisez (facultatif)'"></p>
                <div class="gift-fields">
                    <label>Pour<input type="text" x-model.trim="pour" maxlength="40" placeholder="Prénom du bénéficiaire" autocomplete="off"></label>
                    <label>De la part de<input type="text" x-model.trim="de" maxlength="40" placeholder="Votre prénom" autocomplete="off"></label>
                </div>

                <div class="gift-total">
                    <div>
                        <p class="gift-total__label" x-text="libelle"></p>
                        <p class="gift-total__price"><s class="promo-old" x-show="remise" x-text="tarifNormal(formule) + '€'"></s> <span x-text="prix + '€'"></span></p>
                        <p class="pg-note" x-show="remise" x-text="window.PROMO ? PROMO.label + ' : −' + PROMO.percent + '% sur les cartes « prestation » commandées avant la fin de l’offre' : ''"></p>
                    </div>
                    <div class="gift-total__actions">
                        <a :href="lienWhatsApp" target="_blank" rel="noopener noreferrer" class="pg-btn pg-btn--dark" @click="suivi('whatsapp')"><i class="fa-brands fa-whatsapp"></i> Commander par WhatsApp</a>
                        <a :href="lienSms" class="pg-btn pg-btn--line md:hidden" @click="suivi('sms')"><i class="fa-solid fa-comment-sms"></i> Par SMS</a>
                        <a :href="lienMail" class="pg-btn pg-btn--line" @click="suivi('email')"><i class="fa-regular fa-envelope"></i> Par e-mail</a>
                    </div>
                </div>
                <p class="pg-note">Aucun paiement sur cette page : votre message de commande est déjà rédigé, il ne reste qu'à l'envoyer. Nous vous répondons avec les coordonnées de paiement (Wero ou virement).</p>
            </div>
        </section>

        <section class="pg-section pg-section--alt">
            <div class="pg-wrap">
                <h2 class="pg-h2 reveal">Comment ça marche ?</h2>
                <ol class="pg-steps">
                    <li class="reveal"><span>1</span><h3>Vous commandez</h3><p>Composez la carte ci-dessus et envoyez-nous le message pré-rempli.</p></li>
                    <li class="reveal stagger-1"><span>2</span><h3>Vous réglez</h3><p>Par Wero ou virement instantané, sans frais.</p></li>
                    <li class="reveal stagger-2"><span>3</span><h3>Vous recevez la carte</h3><p>En PDF, avec un code unique, par WhatsApp ou e-mail. À transférer ou à imprimer.</p></li>
                    <li class="reveal stagger-3"><span>4</span><h3>Le bénéficiaire réserve</h3><p>Quand il veut pendant 12 mois. Nous venons chez lui avec tout le matériel.</p></li>
                </ol>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap pg-narrow">
                <h2 class="pg-h2 reveal">Questions fréquentes</h2>
                {{faq}}
                <p class="pg-note">Conditions complètes : <a href="cgv.html#cartes-cadeaux">article « Cartes cadeaux » de nos CGV</a>. Une prise électrique et un point d'eau à proximité du véhicule sont nécessaires le jour de la prestation.</p>
            </div>
        </section>

        <section class="pg-cta">
            <div class="pg-wrap pg-narrow">
                <h2>Un cadeau prêt en quelques minutes</h2>
                <p>Composez la carte, envoyez le message, c'est tout.</p>
                <div class="pg-actions pg-actions--center">
                    <a href="#composer" class="pg-btn pg-btn--light">Composer ma carte <i class="fa-solid fa-arrow-up"></i></a>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Tarifs identiques à ceux du simulateur (services.html) — générés par tools/build_pages.py
        function carteCadeau() {
            return {
                mode: 'formule', vehicule: 'citadine', formule: 'complet', montant: 100, pour: '', de: '',
                vehicules: {{vehicules_js}},
                montants: [50, 80, 100, 150],
                get estMoto() { return this.vehicule === 'moto'; },
                get formules() {
                    return this.estMoto
                        ? [{ id: 'ext', nom: 'Essentiel', detail: 'Lavage sécurisé' }, { id: 'int', nom: 'Détails', detail: 'Chaîne, cadre & moteur' }, { id: 'complet', nom: 'Pack Complet', detail: 'Avec protection' }]
                        : [{ id: 'ext', nom: 'Extérieur', detail: 'Décontamination & brillance' }, { id: 'int', nom: 'Intérieur', detail: 'Rénovation haute précision' }, { id: 'complet', nom: 'Pack Complet', detail: 'Intérieur + extérieur' }];
                },
                promoOn: !!(window.PROMO && window.PROMO.active),
                tarifNormal(f) { return this.vehicules.find(v => v.id === this.vehicule)[f]; },
                // Pendant une offre saisonnière, la remise s'applique aux cartes « prestation ».
                tarif(f) { return window.PROMO ? window.PROMO.apply(this.tarifNormal(f)) : this.tarifNormal(f); },
                get remise() { return this.promoOn && this.mode === 'formule'; },
                get prix() { return this.mode === 'formule' ? this.tarif(this.formule) : this.montant; },
                get libelle() {
                    if (this.mode === 'montant') return 'Carte cadeau de ' + this.montant + '€';
                    const v = this.vehicules.find(x => x.id === this.vehicule).nom;
                    return this.formules.find(f => f.id === this.formule).nom + ' · ' + v;
                },
                get message() {
                    let m = 'Bonjour, je souhaite commander une carte cadeau 🎁\\n\\n' + '• ' + this.libelle + ' : ' + this.prix + '€' + (this.remise ? ' (' + window.PROMO.label + ' −' + window.PROMO.percent + '%, au lieu de ' + this.tarifNormal(this.formule) + '€)' : '') + '\\n';
                    if (this.pour) m += '• Pour : ' + this.pour + '\\n';
                    if (this.de) m += '• De la part de : ' + this.de + '\\n';
                    return m + '\\nMerci de m’indiquer comment régler.';
                },
                get lienWhatsApp() { return 'https://wa.me/33750875964?text=' + encodeURIComponent(this.message); },
                get lienSms() { return 'sms:+33750875964?&body=' + encodeURIComponent(this.message); },
                get lienMail() { return 'mailto:continental.detailing.idf@gmail.com?subject=' + encodeURIComponent('Commande carte cadeau') + '&body=' + encodeURIComponent(this.message); },
                suivi(canal) {
                    if (typeof gtag === 'function') gtag('event', 'carte_cadeau_commande', { canal: canal, valeur: this.prix });
                    if (typeof va === 'function') va('event', { name: 'carte_cadeau_commande', data: { canal: canal, valeur: this.prix } });
                }
            };
        }
        // Mention « Noël » affichée jusqu'au 25 décembre inclus
        (function () {
            var d = new Date();
            if (d.getMonth() === 10 || (d.getMonth() === 11 && d.getDate() <= 25)) {
                document.querySelectorAll('[data-noel]').forEach(function (el) { el.hidden = false; });
            }
        })();
    </script>
'''


def build_cadeau():
    url = SITE + '/carte-cadeau.html'
    vehicules = json.dumps([{'id': k, 'nom': n, 'ext': e, 'int': i, 'complet': c} for k, n, e, i, c in TARIFS],
                           ensure_ascii=False)
    head = render(HEAD, canonical=url,
                  title='Carte cadeau nettoyage voiture à domicile — Essonne & Seine-et-Marne | Continental Detailing',
                  description="Offrez un nettoyage auto premium à domicile : carte cadeau Continental Detailing dès 39€, envoyée par WhatsApp ou e-mail, valable 12 mois en Essonne (91) et Seine-et-Marne (77).",
                  head_extra='    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>\n'
                             + jsonld(faq_schema(GIFT_FAQS)))
    write('carte-cadeau.html', head + render(GIFT_BODY, faq=faq_block(GIFT_FAQS), vehicules_js=vehicules) + FOOT)


# ───────────────────────── Contact ─────────────────────────

CONTACT_BODY = '''
    <main>
        <section class="pg-hero">
            <div class="pg-wrap">
                <p class="pg-eyebrow">Contact</p>
                <h1 class="pg-h1">Écrivez-nous, on vous répond vite</h1>
                <p class="pg-lead">Nous sommes souvent en prestation : le plus rapide est de nous envoyer un message. Dites-nous votre véhicule, la formule souhaitée et votre ville, nous revenons vers vous rapidement.</p>
            </div>
        </section>

        <section class="pg-section">
            <div class="pg-wrap">
                <div class="pg-grid3">
                    <a href="{{wa}}" target="_blank" rel="noopener noreferrer" class="pg-card pg-contact reveal">
                        <i class="fa-brands fa-whatsapp pg-icon"></i><h2 class="pg-h3">WhatsApp</h2>
                        <p>Le moyen le plus rapide. Votre message est déjà rédigé, il ne reste qu'à l'envoyer.</p><span>Ouvrir WhatsApp <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                    <a href="{{sms}}" class="pg-card pg-contact reveal stagger-1">
                        <i class="fa-solid fa-comment-sms pg-icon"></i><h2 class="pg-h3">SMS</h2>
                        <p>07 50 87 59 64. Par message de préférence : nous ne pouvons pas toujours décrocher.</p><span>Envoyer un SMS <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                    <a href="https://www.instagram.com/continental.detailing.idf/" target="_blank" rel="noopener noreferrer" class="pg-card pg-contact reveal stagger-2">
                        <i class="fa-brands fa-instagram pg-icon"></i><h2 class="pg-h3">Instagram</h2>
                        <p>@continental.detailing.idf. Écrivez-nous en message privé et découvrez nos réalisations.</p><span>Voir le profil <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                    <a href="mailto:continental.detailing.idf@gmail.com" class="pg-card pg-contact reveal">
                        <i class="fa-regular fa-envelope pg-icon"></i><h2 class="pg-h3">E-mail</h2>
                        <p>continental.detailing.idf@gmail.com. Idéal pour une demande de devis professionnel.</p><span>Écrire un e-mail <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                    <a href="services.html" class="pg-card pg-contact reveal stagger-1">
                        <i class="fa-solid fa-calculator pg-icon"></i><h2 class="pg-h3">Devis en ligne</h2>
                        <p>Choisissez votre véhicule et votre formule : votre prix s'affiche en deux minutes.</p><span>Calculer mon prix <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                    <a href="professionnels.html" class="pg-card pg-contact reveal stagger-2">
                        <i class="fa-solid fa-building pg-icon"></i><h2 class="pg-h3">Professionnels</h2>
                        <p>Flottes, utilitaires, véhicules d'occasion à préparer : demandez un devis adapté.</p><span>Voir l'offre pro <i class="fa-solid fa-arrow-right"></i></span>
                    </a>
                </div>
            </div>
        </section>

        <section class="pg-section pg-section--alt">
            <div class="pg-wrap pg-two">
                <div class="pg-prose">
                    <h2 class="pg-h2">Informations pratiques</h2>
                    <p><strong>Zone d'intervention :</strong> Essonne (91) et Seine-et-Marne (77), à domicile ou sur votre lieu de travail.</p>
                    <p><strong>Créneaux :</strong> le samedi et le dimanche en journée, et en semaine à partir de 19h. Sur rendez-vous.</p>
                    <p><strong>Sur place :</strong> une prise électrique standard et un point d'eau à proximité du véhicule suffisent. Nous apportons tout le reste.</p>
                    <p><strong>Paiement :</strong> acompte de 40€ par Wero ou virement pour bloquer le créneau, solde après la prestation.</p>
                </div>
                <aside class="pg-card">
                    <h3 class="pg-h3">Villes desservies</h3>
                    <p>{{villes}} et les communes voisines.</p>
                    <p style="margin-top:14px;">Continental Detailing · micro-entreprise basée au Mée-sur-Seine (77) · SIRET 100 916 949 00017</p>
                </aside>
            </div>
        </section>
    </main>
'''


def build_contact():
    url = SITE + '/contact.html'
    message = 'Bonjour, je souhaite un renseignement pour le nettoyage de ma voiture 🚗\nVéhicule : \nFormule : \nVille : '
    schema = jsonld({
        '@context': 'https://schema.org', '@type': 'ContactPage', 'url': url,
        'name': 'Contact — Continental Detailing',
        'mainEntity': {'@id': SITE + '/#localbusiness'},
    })
    villes = ', '.join('<a href="nettoyage-voiture-domicile-' + v['slug'] + '.html">' + v['nom'] + '</a>' for v in VILLES)
    head = render(HEAD, canonical=url,
                  title='Contact — WhatsApp, SMS, e-mail | Continental Detailing',
                  description="Contactez Continental Detailing par WhatsApp, SMS, Instagram ou e-mail : nettoyage et detailing auto à domicile en Essonne (91) et Seine-et-Marne (77), le week-end et en soirée.",
                  head_extra=schema)
    write('contact.html', head + render(CONTACT_BODY, wa=wa(message),
                                        sms='sms:+33750875964?&body=' + urllib.parse.quote(message), villes=villes) + FOOT)


if __name__ == '__main__':
    build_villes()
    build_pro()
    build_cadeau()
    build_contact()
