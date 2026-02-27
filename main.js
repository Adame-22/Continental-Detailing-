
document.addEventListener('alpine:init', () => {
    Alpine.data('bookingForm', () => ({
        clientType: 'particulier', // 'particulier' ou 'pro'
        vehicule: 'citadine',
        formule: 'complet',
        options: { poils: false, non_videe: false, cire: false },
        paiement: 'cb', 
        showGuide: false, 
        
        numeroContact: '33750875964', 
        compteInsta: 'continental_detailing', 
        
        tarifs: {
            citadine: { ext: 49, int: 79, complet: 119, nom: 'Citadine' },
            berline: { ext: 59, int: 89, complet: 129, nom: 'Berline' },
            suv: { ext: 69, int: 99, complet: 139, nom: 'SUV' },
            mono5: { ext: 79, int: 109, complet: 149, nom: 'Monospace 5pl' },
            mono7: { ext: 89, int: 119, complet: 159, nom: 'Monospace 7pl' }
        },
        nomsFormules: { ext: 'Lavage Extérieur', int: 'Lavage Intérieur', complet: 'Pack Complet' },
        nomsPaiement: { especes: 'Espèces', cb: 'Carte Bancaire (Sur place)', ligne: 'Paiement en ligne (Lien)' },
        
        get isUtilitaire() { return this.vehicule === 'util'; },
        
        get totalPrix() {
            if (this.isUtilitaire || this.clientType === 'pro') return 0;
            let t = this.tarifs[this.vehicule][this.formule];
            if (this.options.poils) t += 20;
            if (this.options.non_videe) t += 10;
            if (this.options.cire) t += 30;
            return t;
        },

        get texteMessage() {
            if (this.clientType === 'pro') {
                return encodeURIComponent('Bonjour Continental Detailing, je représente une entreprise et je souhaiterais obtenir un devis pour l'entretien de nos véhicules professionnels.\n\nPouvons-nous en discuter ?');
            }

            if (this.isUtilitaire) {
                return encodeURIComponent('Bonjour Continental Detailing, je souhaite obtenir un devis sur-mesure pour mon véhicule utilitaire.\n\nType d'utilitaire (ex: L1H1, Benne, etc) : \nÉtat général : \n\nQuelles sont vos disponibilités ?');
            }

            let msg = 'Bonjour Continental Detailing, je souhaite planifier une intervention :\n\n';
            msg += '🚗 Véhicule : ' + this.tarifs[this.vehicule].nom + '\n';
            msg += '✨ Formule : ' + this.nomsFormules[this.formule] + ' (' + this.tarifs[this.vehicule][this.formule] + '€)\n';
            
            let optsSelectionnees = [];
            if(this.options.poils) optsSelectionnees.push('Poils/Très sale (+20€)');
            if(this.options.non_videe) optsSelectionnees.push('Véhicule pas vidé (+10€)');
            if(this.options.cire) optsSelectionnees.push('Cire Express (+30€)');
            
            if(optsSelectionnees.length > 0) msg += '➕ Options : ' + optsSelectionnees.join(', ') + '\n';
            
            msg += '\n💰 TOTAL ESTIMÉ : ' + this.totalPrix + ' €\n';
            msg += '💳 Règlement souhaité : ' + this.nomsPaiement[this.paiement] + '\n';
            if(this.paiement === 'ligne') msg += '(Merci de m'envoyer un lien de paiement sécurisé pour bloquer le RDV).\n';

            msg += '\nQuelles sont vos disponibilités ?';
            return encodeURIComponent(msg);
        },
        
        get lienWhatsApp() { return 'https://wa.me/' + this.numeroContact + '?text=' + this.texteMessage; },
        get lienSMS() { return 'sms:+' + this.numeroContact + '?body=' + this.texteMessage; },
        get lienInsta() { return 'https://instagram.com/' + this.compteInsta; }
    }));
});
