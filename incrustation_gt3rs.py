import re
import base64
import glob
import os

# Find the latest generated images
ext_images = glob.glob(r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\gt3rs_exterior_*.png")
int_images = glob.glob(r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\gt3rs_interior_*.png")
full_images = glob.glob(r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\gt3rs_full_*.png")

ext_img = max(ext_images, key=os.path.getctime)
int_img = max(int_images, key=os.path.getctime)
full_img = max(full_images, key=os.path.getctime)

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

ext_b64 = get_b64(ext_img)
int_b64 = get_b64(int_img)
full_b64 = get_b64(full_img)

# Open current HTML
with open('flyer_base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern for a generic pricing card block
# We'll identify them by their titles
# Since the first two might now look identical because of previous failed runs,
# we search for the specific titles: "Extérieur", "Intérieur", "Signature"

# 1. FIX EXTERIEUR CARD
# Target the first card (Extérieur)
ext_card_pattern = r'<div class="flex-1 rounded-2xl p-4 gold-bg-light flex flex-col">.*?<h2 class="text-\[32px\] font-black text-white uppercase tracking-wider">Extérieur</h2>.*?</ul>\s*</div>'
ext_replacement = f'''<div class="flex-1 rounded-2xl p-4 gold-bg-light flex flex-col">
                    <!-- Incrustation -->
                    <div class="w-full h-[180px] rounded-xl overflow-hidden mb-5 border-2 border-gold/40 shadow-lg relative group">
                        <img src="data:image/jpeg;base64,{ext_b64}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    </div>
                    <div class="text-center mb-4">
                        <i class="fa-solid fa-car-side text-[38px] text-gold mb-2"></i>
                        <h2 class="text-[32px] font-black text-white uppercase tracking-wider">Extérieur</h2>
                    </div>
                    <ul class="gold-bullets text-[19px] text-stone-200 leading-snug font-medium px-2">
                        <li>Prélavage actif (Snow Foam)</li>
                        <li>Nettoyage jantes & passages</li>
                        <li>Lavage manuel 2 seaux</li>
                        <li>Décontamination carrosserie</li>
                        <li>Dressing pneumatiques</li>
                    </ul>
                </div>'''

# Replace only the first one
html = re.sub(ext_card_pattern, ext_replacement, html, count=1, flags=re.DOTALL)

# 2. FIX INTERIEUR CARD
# Target the second card which might currently have the "Extérieur" title if duplicate, 
# or might have "Intérieur" if it was original.
# We'll target the SECOND card block by looking for the one after the first </div>
int_card_pattern = r'</div>\s*<div class="flex-1 rounded-2xl p-4 gold-bg-light flex flex-col">.*?<h2 class="text-\[32px\] font-black text-white uppercase tracking-wider">Extérieur</h2>.*?</ul>\s*</div>'
int_replacement = f'''</div>
                
                <div class="flex-1 rounded-2xl p-4 gold-bg-light flex flex-col" style="border-left: 1px solid rgba(196,165,93,0.15); border-right: 1px solid rgba(196,165,93,0.15);">
                    <!-- Incrustation -->
                    <div class="w-full h-[180px] rounded-xl overflow-hidden mb-5 border-2 border-gold/40 shadow-lg relative group">
                        <img src="data:image/jpeg;base64,{int_b64}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    </div>
                    <div class="text-center mb-4">
                        <i class="fa-solid fa-spray-can-sparkles text-[38px] text-gold mb-2"></i>
                        <h2 class="text-[32px] font-black text-white uppercase tracking-wider">Intérieur</h2>
                    </div>
                    <ul class="gold-bullets text-[19px] text-stone-200 leading-snug font-medium px-2">
                        <li>Aspiration minutieuse (habitacle)</li>
                        <li>Dégraissage plastiques pinceau</li>
                        <li>Shampoing moquettes & tapis</li>
                        <li>Nettoyage profond (cuir/tissu)</li>
                        <li>Vitres intérieures sans trace</li>
                    </ul>
                </div>'''

html = re.sub(int_card_pattern, int_replacement, html, count=1, flags=re.DOTALL)

# 3. FIX SIGNATURE CARD
# Target the third card (Signature)
sig_card_pattern = r'<div class="flex-1 rounded-2xl p-4" style="background: rgba\(168,136,74,0\.10\);">.*?<h2 class="text-\[32px\] font-black gold-gradient-text uppercase tracking-wider">Signature</h2>.*?</ul>.*?</div>\s*</div>'
sig_replacement = f'''<div class="flex-1 rounded-2xl p-4 flex flex-col relative" style="background: rgba(168,136,74,0.10); border: 1px solid rgba(196,165,93,0.3);">
                    <div class="absolute -top-4 -right-2 bg-gold text-black font-bold py-1 px-4 rounded-full text-[15px] transform rotate-12 shadow-lg z-20 border border-yellow-200">RECOMMANDÉ</div>
                    <!-- Incrustation -->
                    <div class="w-full h-[180px] rounded-xl overflow-hidden mb-5 border-2 border-gold/60 shadow-[0_0_15px_rgba(196,165,93,0.3)] relative group">
                        <img src="data:image/jpeg;base64,{full_b64}" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    </div>
                    <div class="text-center mb-4 relative">
                        <i class="fa-solid fa-crown text-[38px] text-gold mb-2"></i>
                        <h2 class="text-[32px] font-black gold-gradient-text uppercase tracking-wider">Signature</h2>
                    </div>
                    <ul class="gold-bullets text-[19px] text-white font-bold leading-snug px-2">
                        <li class="text-gold">Toutes les prestations Intérieur</li>
                        <li class="text-gold">Toutes les prestations Extérieur</li>
                        <li>Cire de protection Brillance</li>
                        <li>Soin protecteur plastiques anti-UV</li>
                    </ul>
                </div>'''

html = re.sub(sig_card_pattern, sig_replacement, html, count=1, flags=re.DOTALL)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Incrustations GT3 RS corrigées et appliquées !")
