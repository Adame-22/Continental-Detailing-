
# Continental Detailing Website Blueprint

## 1. Overview

This document outlines the structure, design, and features of the Continental Detailing website. The website is a single-page application designed to showcase the company's car cleaning services and allow users to easily configure and book a service.

## 2. Project Structure

The project consists of the following files:

- `index.html`: The main landing page of the website.
- `services.html`: A dynamic page for both quotes and service booking.
- `style.css`: A file for custom CSS (though most styling is done via Tailwind CSS).
- `main.js`: A JavaScript file containing the logic for the `services.html` page.
- `blueprint.md`: This document.

## 3. Design and Features

### 3.1. Overall Design

- **Color Palette:** The design uses a sophisticated, dark-themed palette:
  - `navy: '#050B14'` (deep blue-black)
  - `navylight: '#0A1128'` (dark navy blue)
  - `gold: '#D4AF37'` (rich gold)
  - `goldlight: '#F3E5AB'` (light gold)
- **Typography:**
  - **Headings:** `Playfair Display`, a serif font, for an elegant, premium feel.
  - **Body:** `Inter`, a sans-serif font, for clean readability.
- **UI Elements:**
  - **Cards:** Modern, rounded cards with blur effects and subtle borders (`bg-navylight/60`, `backdrop-blur-xl`, `border-white/5`).
  - **Buttons:** Interactive buttons with smooth transitions (`ui-transition`).
  - **Logo:** A code-based logo with a stylized shield icon and the company name, using a gold gradient.

### 3.2. `index.html` - Main Page

- **Header:** A sticky navigation bar with the logo, links to "Accueil" and "Tarifs & Réservation," and a "Contact" button.
- **Hero Section:** A full-width section with a background image, a bold headline, and a call-to-action button.
- **Value Propositions:** A three-card layout highlighting the company's key strengths.
- **How It Works:** A simple three-step guide to the booking process.
- **Footer:** Includes copyright information and a link to the company's Instagram page (`continental_detailing`).

### 3.3. `services.html` - Quote and Booking Page (Major Update)

This page has been redesigned to cater to two distinct client types: **Particulier** (Individual) and **Entreprise** (Business), with a special workflow for utility vehicles.

- **Client Type Selector:** A prominent toggle at the top allows users to switch between "Particulier" and "Entreprise" views.

- **"Entreprise" (B2B) View:**
  - Displays a professional-looking section highlighting the benefits of B2B services (Pro Invoicing, On-site intervention, Tiered pricing).
  - The call-to-action is simplified to a single "Demander un devis B2B" button, which opens a pre-filled WhatsApp message for a custom quote.

- **"Particulier" (Individual) View:**
  - **Standard Booking Flow:** Contains the familiar step-by-step process.
  - **Vehicle Selection:** Includes "Utilitaire" (Utility Vehicle) as an option.
    - **Utility Vehicle Logic:** If "Utilitaire" is selected, the pricing and options sections are hidden. A dedicated card appears explaining that a custom quote is required, with a button to request it via WhatsApp.
  - **Service Selection:** Standard options for Extérieur, Intérieur, and Pack Complet.
  - **Supplements:** Options for extra services like "Poils d'animaux, Véhicule très sale, Sable", "Véhicule pas vidé", and "Cire Céramique Express".
  - **Payment Section:** Choice of payment methods.

- **Dynamic Booking Bar:**
  - For **Entreprise** or **Utilitaire** selections, the bar shows "Sur Devis" and the button says "Demander devis".
  - For standard **Particulier** selections, it displays the total price and the button says "Réserver".

## 4. Current Task: Fix `services.html` Page

The user reported that the `services.html` page was not working correctly when opened in a new window. This was likely due to an unstable version of a third-party library (Alpine.js).

- **Actions Taken:**
  1.  **`main.js` Created:** The JavaScript logic from `services.html` was moved to a new `main.js` file for better organization.
  2.  **`services.html` Updated:** The page was updated to use a specific, stable version of Alpine.js (`3.13.3`) and to include the new `main.js` script.
  3.  **`blueprint.md` Updated:** This document was updated to reflect the changes to the project structure and the fix that was implemented.

- **Result:** The `services.html` page should now be stable and work correctly in all browsing contexts. The code is also better organized, which will make future updates easier.
