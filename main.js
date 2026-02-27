
document.addEventListener('alpine:init', () => {
    Alpine.data('bookingForm', () => ({
        // State
        clientType: 'particulier', // 'particulier' or 'pro'
        vehicule: 'citadine',
        formule: 'complet',
        options: { poils: false, non_videe: false, cire: false },
        paiement: 'cb',
        showGuide: false,

        // Configuration
        numeroContact: '33750875964',
        compteInsta: 'continental_detailing',

        vehiculeTypes: {
            citadine: { nom: 'Citadine', icon: 'fa-car-side', tarifs: { ext: 49, int: 79, complet: 119 } },
            berline: { nom: 'Berline', icon: 'fa-car', tarifs: { ext: 59, int: 89, complet: 129 } },
            suv: { nom: 'SUV', icon: 'fa-truck-pickup', tarifs: { ext: 69, int: 99, complet: 139 } },
            mono5: { nom: 'Monospace 5pl', icon: 'fa-van-shuttle', tarifs: { ext: 79, int: 109, complet: 149 } },
            mono7: { nom: 'Monospace 7pl', icon: 'fa-van-shuttle', tarifs: { ext: 89, int: 119, complet: 159 } },
            util: { nom: 'Utilitaire', icon: 'fa-truck', tarifs: null }
        },

        formuleTypes: {
            ext: { nom: 'Extérieur', desc: 'Prélavage mousse, jantes, séchage, brillance pneus.' },
            complet: { nom: 'Pack Complet', desc: 'Remise à neuf : nettoyage intérieur/extérieur avec pressing inclus.', bestseller: true },
            int: { nom: 'Intérieur', desc: 'Aspiration, pressing des sièges, plastiques et vitres.' }
        },
        
        optionTypes: [
            { key: 'poils', text: 'Poils d'animaux, Véhicule très sale, Sable', price: 20 },
            { key: 'non_videe', text: 'Véhicule pas vidé', price: 10, tooltip: 'Merci de vider vos effets personnels.' },
            { key: 'cire', text: 'Cire Céramique Express', subtext: 'Brillance extrême (3 mois)', price: 30 }
        ],

        paiementTypes: {
            cb: { nom: 'Carte Bancaire', desc: 'Sur place contact/sans-contact', icon: 'fa-credit-card' },
            especes: { nom: 'Espèces', desc: 'L'appoint est recommandé', icon: 'fa-money-bill-wave' },
            ligne: { nom: 'En ligne (Lien)', desc: 'Lien sécurisé avant RDV', icon: 'fa-link' }
        },

        // Getters / Computed Properties
        get isUtilitaire() { return this.vehicule === 'util'; },
        
        get totalPrix() {
            if (this.isUtilitaire || this.clientType === 'pro') return 0;
            
            let tarifFormule = this.vehiculeTypes[this.vehicule]?.tarifs?.[this.formule] ?? 0;
            
            let tarifOptions = this.optionTypes.reduce((acc, opt) => {
                return acc + (this.options[opt.key] ? opt.price : 0);
            }, 0);

            return tarifFormule + tarifOptions;
        },

        get texteMessage() {
            if (this.clientType === 'pro') {
                return encodeURIComponent('Bonjour Continental Detailing, je représente une entreprise et je souhaiterais obtenir un devis pour l'entretien de nos véhicules professionnels.\n\nPouvons-nous en discuter ?');
            }

            if (this.isUtilitaire) {
                return encodeURIComponent('Bonjour Continental Detailing, je souhaite obtenir un devis sur-mesure pour mon véhicule utilitaire.\n\nType d'utilitaire (ex: L1H1, Benne, etc) : \nÉtat général : \n\nQuelles sont vos disponibilités ?');
            }

            let vehiculeData = this.vehiculeTypes[this.vehicule];
            let formuleData = this.formuleTypes[this.formule];
            
            let msg = 'Bonjour Continental Detailing, je souhaite planifier une intervention :\n\n';
            msg += `🚗 Véhicule : ${vehiculeData.nom}\n`;
            msg += `✨ Formule : ${formuleData.nom} (${vehiculeData.tarifs[this.formule]}€)\n`;
            
            let optsSelectionnees = this.optionTypes
                .filter(opt => this.options[opt.key])
                .map(opt => `${opt.text.split(',')[0]} (+${opt.price}€)`);
            
            if (optsSelectionnees.length > 0) {
                msg += `➕ Options : ${optsSelectionnees.join(', ')}\n`;
            }
            
            msg += `\n💰 TOTAL ESTIMÉ : ${this.totalPrix} €\n`;
            msg += `💳 Règlement souhaité : ${this.paiementTypes[this.paiement].nom}\n`;
            
            if (this.paiement === 'ligne') {
                msg += '(Merci de m'envoyer un lien de paiement sécurisé pour bloquer le RDV).\n';
            }

            msg += '\nQuelles sont vos disponibilités ?';
            return encodeURIComponent(msg);
        },
        
        get lienWhatsApp() { return `https://wa.me/${this.numeroContact}?text=${this.texteMessage}`; },
        get lienSMS() { return `sms:+${this.numeroContact}?body=${this.texteMessage}`; },
        get lienInsta() { return `https://instagram.com/${this.compteInsta}`; },

        // Helper methods
        getVehiculeTypesArray() {
            return Object.entries(this.vehiculeTypes).map(([key, value]) => ({ key, ...value }));
        },
        getFormuleTypesArray() {
            return Object.entries(this.formuleTypes).map(([key, value]) => ({ key, ...value }));
        },
        getPaiementTypesArray() {
            return Object.entries(this.paiementTypes).map(([key, value]) => ({ key, ...value }));
        }
    }));
});
