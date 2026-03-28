---
description: [Continental Detailing] Reprendre le développement du projet
---

# 🚗 Continental Detailing - Dossier de Référence

Ce document sert de "mémoire centrale" à l'agent (moi) pour éviter de se perdre lors de tes prochaines sessions. **Dès que l'utilisateur te demande de reprendre Continental Detailing, tu dois lire ce fichier pour être à jour.**

## 1. Description du Projet
- **Nom** : Continental Detailing
- **Activité** : Service de nettoyage automobile Premium et Detailing (Essonne 91 & Seine-et-Marne 77). Interventions à domicile ou sur le lieu de travail avec matériel électrique & silencieux (éco-responsable).
- **Design** : "Premium Dark Mode" (Fond bleu nuit `#0F172A`, accents bleu vif `#38BDF8`). L'objectif est d'inspirer le haut de gamme.

## 2. Structure Technique
- **Technologies** : HTML5, CSS3, Tailwind CSS (via script CDN pour le dev), Alpine.js (pour la logique du simulateur) et FontAwesome 6.5.1 pour les pictogrammes.
- **Fichiers clés** :
  - `index.html` : Landing page principale avec accroche, récapitulatif des formules ("Lavage Intérieur" et "Décontamination Extérieur") et avantages clés.
  - `services.html` : Page du simulateur de tarifs interactif avec Alpine.js. Calcule le devis auto et génère un ticket WhatsApp.
  - `css/style.css` : Fichier CSS custom, contenant les variables racines de couleurs et les animations (classes `.ui-transition`, `.btn-primary`).

## 3. Grille Tarifaire à jour (Définitive)

**Les Formules :**
- `ext` : Lavage Extérieur (Prélavage, technique des 2 seaux, jantes, dressing pneus)
- `int` : Lavage Intérieur (Aspiration, pressing, plastiques, vitres, cuir)
- `complet` : Pack Complet (Intérieur + Extérieur = Remise appliquée)

**Les Tailles de Véhicules & Prix (€) :**
- **Citadine** -> Ext: 49€ | Int: 79€ | Complet: 119€
- **Berline** -> Ext: 59€ | Int: 89€ | Complet: 129€
- **SUV** -> Ext: 69€ | Int: 99€ | Complet: 139€
- **Monospace 5 places** -> Ext: 79€ | Int: 109€ | Complet: 149€
- **Monospace 7 places** -> Ext: 89€ | Int: 119€ | Complet: 159€
- **Utilitaires** -> Sur Devis Uniquement.

**Les Options :**
- Poils d'animaux / État critique : +20€
- Véhicule non vidé : +10€
- Cire de protection hydrophobe : +30€

## 4. Statut Hébergement & DNS
- **Hébergement** : Code hébergé sur GitHub, déployé automatiquement via Vercel.
- **Nom de domaine** : `continentaldetailing.fr` (Acheté sur IONOS).
- **DNS** : Pointage via A record (`76.76.21.21`) et CNAME (`www -> cname.vercel-dns.com`) configuré et fonctionnel.

## 5. Prochaines Étapes / Évolutions Envisagées
- Remplacer les images "Unsplash" par de **vraies photos** des interventions du client.
- Ajouter une section "Galerie" / Avant-Après pour la preuve sociale.
- Ajouter un formulaire e-mail en complément si le client ne souhaite pas utiliser WhatsApp.
