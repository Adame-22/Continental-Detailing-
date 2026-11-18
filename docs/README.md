# Continental Detailing — carnet de bord

Ce dossier garde ce qui ne se voit pas dans le code : les décisions, les textes
prêts à copier et l'état de la prospection. Il n'est pas mis en ligne (voir
`.vercelignore`). Le suivi des prospects, lui, vit dans Google Drive, dans le
fichier `CRM_Prospects_Continental_Detailing`.

Dernière mise à jour : 18 novembre 2026.

## Le site

| Page | Rôle |
|---|---|
| `index.html`, `services.html`, `about.html`, `avis.html` | Pages principales, écrites à la main |
| `carte-cadeau.html`, `professionnels.html`, `contact.html` | Générées par `tools/build_pages.py` |
| `nettoyage-voiture-domicile-<ville>.html` | Six pages par ville, générées par le même script |
| `acompte.html`, `reglement.html` | Paiement par Wero ou virement (non indexées) |
| `outil-carte-cadeau.html` | Outil interne pour éditer une carte cadeau en PDF (non indexé) |

Pour changer un prix ou un texte des pages générées : modifier
`tools/build_pages.py`, lancer `python3 tools/build_pages.py`, puis valider les
fichiers `.html` produits. Les tarifs y sont recopiés depuis le simulateur de
`services.html` : les deux doivent rester identiques.

Réglages qui s'éteignent tout seuls, dans `js/promo.js` :

- l'Offre Automne (−20 %) s'est arrêtée le 31 octobre 2026 ;
- le bandeau « Noël : offrez une carte cadeau » s'arrête le 25 décembre 2026.

## Disponibilités

Samedi et dimanche en journée, en semaine à partir de 19 h. Priorité aux
samedis. Les soirs de semaine conviennent surtout à un nettoyage intérieur
(il fait nuit en hiver). Les données lues par Google indiquent 19 h–22 h en
semaine : à ajuster si l'heure de fin réelle est différente.

Capacité d'un samedi : 2 packs complets, ou 3 à 4 prestations simples.

## Décisions prises

- Carte cadeau : valable 12 mois, utilisable en une fois, montants libres de
  50, 80, 100 et 150 €, paiement par Wero ou virement. Conditions dans
  l'article 15 des CGV.
- Offre senior à Ris-Orangis : « Les Samedis Séniors », réservée aux habitants
  de 65 ans et plus, le samedi sur rendez-vous. Extérieur 25 € (45 min),
  intérieur 35 € (1 h), complet 55 € (1 h 45), SUV et monospace 10 € de plus.
  La durée plafonnée est la condition du prix. Flyers dans
  `marketing/flyers/` (versions claire et sombre). L'ancien Pass Sénior
  (−35 %, dès 32 €, `pass-senior.png`) n'est plus à envoyer.
- Acompte de 40 € par Wero ou virement (le bouton « carte bancaire » ne
  fonctionnait pas ; il faudrait un lien Stripe ou SumUp pour le remettre).
- Statistiques : Google Analytics ne se charge qu'après accord (bannière
  cookies). Vercel Web Analytics est installé dans le code mais reste à
  activer dans Vercel (projet `continental-detailing`, onglet Analytics).

## En attente d'une décision

- **Offre pour les entreprises.** Proposé : premier véhicule à −50 % (pack
  complet à 59 € au lieu de 119 €). L'essai gratuit a déjà été proposé par
  e-mail en juillet 2026, sans résultat.
- **Adresse d'envoi.** `info@continentaldetailing.fr` : à confirmer qu'elle
  reçoit bien les e-mails avant de la mettre sur le site et dans Brevo.
- **Recherche d'adresses via Apollo.** 1 crédit par adresse trouvée.

## Prospection : où on en est

- Juin–juillet 2026 : une trentaine d'e-mails (mairies avec l'offre senior,
  agences immobilières, garages, VTC). Une dizaine d'adresses devinées
  n'existaient pas.
- Deux mairies ont répondu favorablement et transmis l'offre senior à leur
  CCAS et à leur service Communication : Ris-Orangis (17 juin) et
  Savigny-le-Temple (8 juillet). Aucune relance n'a suivi.
- 12 novembre 2026 : relances envoyées à trois prospects de juillet, un
  premier e-mail à un nouveau garage, et relance des deux mairies.
- 13 novembre 2026 : le cabinet du maire de Savigny-le-Temple a transmis au
  service concerné, qui doit rappeler. L'adresse de la stagiaire qui avait
  répondu en juillet n'existe plus : écrire au cabinet du maire seulement.
- 17 novembre 2026 : la mairie de Ris-Orangis a redemandé le flyer. L'ancien
  Pass Sénior est parti par erreur le soir même.
- 18 novembre 2026 : correctif envoyé à la mairie avec le flyer définitif
  « Samedis Séniors », en demandant de ne pas diffuser le précédent.

Suite prévue : demander à Ris-Orangis où et quand le flyer sera diffusé
(vers le 24 novembre) ; appeler le CCAS de Savigny-le-Temple sans nouvelles
le 26 novembre.

Règles à tenir :

- prospection par e-mail réservée aux professionnels et aux collectivités,
  avec une phrase pour ne plus être contacté ;
- adresses vérifiées plutôt que devinées ;
- un seul tableau de suivi (le CRM dans Drive), mis à jour à chaque envoi,
  pour ne jamais écrire deux fois à la même personne.

## Textes prêts à copier

### WhatsApp Business

Message d'accueil :

```
Bonjour et merci pour votre message ! 👋

Je suis Continental Detailing, nettoyage auto premium à domicile en Essonne (91) et Seine-et-Marne (77).

Pour vous répondre au plus vite, dites-moi :
🚗 Votre véhicule (citadine, berline, SUV…)
✨ La formule souhaitée (extérieur, intérieur ou complet)
📍 Votre ville
📅 Vos disponibilités (samedi, dimanche ou en semaine après 19h)

Tarifs et simulateur : continentaldetailing.fr
Je vous réponds très rapidement !
```

Message d'absence :

```
Merci pour votre message ! 🙏

Je suis actuellement en prestation et ne peux pas répondre tout de suite. Je reviens vers vous dès que possible.

En attendant, vous pouvez estimer votre tarif en 2 minutes ici : continentaldetailing.fr/services.html
```

Réponse rapide `/rdv` :

```
Parfait ! Pour bloquer votre créneau 📅

1️⃣ On fixe ensemble la date et l'heure (samedi, dimanche ou en semaine après 19h)
2️⃣ Vous réglez un acompte de 40€ par Wero ou virement ici : continentaldetailing.fr/acompte.html (il est déduit du total)
3️⃣ Le solde se règle après la prestation

Quelle date vous arrangerait ?
```

Réponse rapide `/infos` :

```
Quelques infos pratiques 🧽

📍 Je viens chez vous ou sur votre lieu de travail
🔌 J'ai seulement besoin d'une prise électrique standard et d'un point d'eau à proximité (j'apporte rallonges et tuyaux)
⏱️ Durée : 2-3 h pour un intérieur ou un extérieur, 4-5 h pour un pack complet
🧴 Produits pH neutre, méthode 2 seaux
```

### Fiche pour les annuaires (Pages Jaunes, StarOfService, Aladom)

- Nom : Continental Detailing
- Exploitant : Adame Zahaf (micro-entreprise), SIRET 100 916 949 00017, APE 4520A
- Siège : Rue du Bois Guyot, 77350 Le Mée-sur-Seine
- Téléphone : 07 50 87 59 64 (par message de préférence)
- E-mail : continental.detailing.idf@gmail.com
- Site : https://continentaldetailing.fr
- Horaires : samedi et dimanche 8 h–20 h, lundi à vendredi à partir de 19 h
- Zone : Essonne (91) et Seine-et-Marne (77)

Description courte :

> Nettoyage et detailing automobile premium à domicile en Essonne (91) et
> Seine-et-Marne (77). Intérieur, extérieur ou pack complet, réalisé à la main
> chez vous, le week-end ou en soirée. Dès 49€.

### E-mail de prospection aux entreprises (brouillon, prix à valider)

Objet : Vos véhicules nettoyés le samedi, sur votre parking

```
Bonjour,

Je suis Adame, de Continental Detailing, au Mée-sur-Seine. Je nettoie les véhicules d'entreprise directement sur place, le samedi, quand ils sont à l'arrêt : aucune immobilisation en semaine.

[OFFRE À VALIDER]

Un samedi vous conviendrait ? Répondez à ce message ou écrivez-moi au 07 50 87 59 64.

Adame Zahaf, Continental Detailing
continentaldetailing.fr/professionnels.html

Si vous ne souhaitez plus recevoir mes messages, répondez « stop ».
```
