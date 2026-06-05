def update_services_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Intérieur Card
    old_card_in = '''<div class="p-8 md:p-10 card-hover-lift reveal-left"
                 style="background:#FFFFFF; border:1px solid rgba(0,0,0,0.08); border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.04);">
                <div class="flex items-start gap-4 mb-8">
                    <div class="w-12 h-12 flex items-center justify-start flex-shrink-0" style="border:1px solid rgba(0,0,0,0.1); border-radius:12px; background: #F9F9F9;">
                        <i class="fa-solid fa-couch text-base" style="color:#1A1A1E;"></i>
                    </div>
                    <div>
                        <h3 class="font-semibold text-primary text-xl">Lavage Intérieur</h3>
                        <p class="text-xs tracking-wider uppercase mt-1" style="color:#1A1A1E;">Rénovation Haute Précision</p>
                    </div>
                </div>'''
    
    new_card_in = '''<div class="card-hover-lift reveal-left flex flex-col"
                 style="background:#FFFFFF; border:1px solid rgba(0,0,0,0.08); border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.04); overflow:hidden;">
                
                <div class="w-full h-56 md:h-72 relative">
                    <img src="images/service-interior.png" class="w-full h-full object-cover" alt="Lavage Intérieur">
                </div>

                <div class="p-8 md:p-10 flex-1">
                    <div class="mb-8">
                        <h3 class="font-bold text-primary text-3xl">Lavage Intérieur</h3>
                        <p class="text-xs tracking-wider uppercase mt-2" style="color:#1A1A1E;">Rénovation Haute Précision</p>
                    </div>'''
    
    if old_card_in in content:
        content = content.replace(old_card_in, new_card_in)
    else:
        # Fallback if there are minor formatting differences, let's just do a simpler replace.
        print("Could not find exact interior card block.")

    # Extérieur Card
    old_card_ex = '''<div class="p-8 md:p-10 card-hover-lift reveal-right"
                 style="background:#FFFFFF; border:1px solid rgba(0,0,0,0.08); border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.04);">
                <div class="flex items-start gap-4 mb-8">
                    <div class="w-12 h-12 flex items-center justify-start flex-shrink-0" style="border:1px solid rgba(0,0,0,0.1); border-radius:12px; background: #F9F9F9;">
                        <i class="fa-solid fa-spray-can text-base" style="color:#1A1A1E;"></i>
                    </div>
                    <div>
                        <h3 class="font-semibold text-primary text-xl">Lavage Extérieur</h3>
                        <p class="text-xs tracking-wider uppercase mt-1" style="color:#1A1A1E;">Décontamination & Brillance</p>
                    </div>
                </div>'''

    new_card_ex = '''<div class="card-hover-lift reveal-right flex flex-col"
                 style="background:#FFFFFF; border:1px solid rgba(0,0,0,0.08); border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,0.04); overflow:hidden;">
                
                <div class="w-full h-56 md:h-72 relative">
                    <img src="images/service-exterior.png" class="w-full h-full object-cover" alt="Lavage Extérieur">
                </div>

                <div class="p-8 md:p-10 flex-1">
                    <div class="mb-8">
                        <h3 class="font-bold text-primary text-3xl">Lavage Extérieur</h3>
                        <p class="text-xs tracking-wider uppercase mt-2" style="color:#1A1A1E;">Décontamination & Brillance</p>
                    </div>'''
    
    if old_card_ex in content:
        content = content.replace(old_card_ex, new_card_ex)
    else:
        print("Could not find exact exterior card block.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_services_cards('index.html')
