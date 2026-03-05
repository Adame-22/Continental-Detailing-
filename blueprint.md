# Project Blueprint

## Overview

This project is a web application for "Continental Detailing," a car detailing service. The main feature is an interactive price calculator that allows users to get a quote and book a service.

## Project Structure

- `public/`: This directory contains all the static assets for the project.
  - `index.html`: The main HTML file, which contains the price calculator application.
- `firebase.json`: The Firebase configuration file, pointing to the `public` directory.
- `blueprint.md`: This file, documenting the project structure and changes.

## Application Details

- **Frameworks:** The application is built using Tailwind CSS and Alpine.js.
- **Functionality:**
    - Users can select their vehicle type, the desired service (interior, exterior, or complete), and any additional options.
    - The application dynamically calculates the total price based on the user's selections.
    - Users can choose between different payment methods.
    - The application generates a pre-filled WhatsApp or SMS message to facilitate booking.
    - There is a separate section for B2B inquiries.
