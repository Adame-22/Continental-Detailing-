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

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Extérieur Column
ext_pattern = r'<div class="flex-1 rounded-2xl p-4 gold-bg-light">\s*<div class="text-center mb-4">\s*<i class="fa-solid fa-car-side text-\[44px\] text-gold mb-3"></i>\s*<h2 class="text-\[32px\] font-black text-white uppercase tracking-wider">Extérieur</h2>\s*</div>\s*<ul class="gold-bullets text-xl text-stone-300 leading-snug">.*?</ul>\s*</div>'

ext_replacement = f'''<div class="flex-1 rounded-2xl p-5 relative overflow-hidden group border border-white/10 shadow-xl" style="background: #09090b;">
                    <img src="data:image/png;base64,{ext_b64}" class="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-lighten filter contrast-125 brightness-110 transition-transform duration-1000 group-hover:scale-110">
                    <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-black/50 to-black/90 z-0"></div>
                    <div class="relative z-10">
                        <div class="text-center mb-4">
                            <i class="fa-solid fa-car-side text-[44px] text-gold mb-3 drop-shadow-md"></i>
                            <h2 class="text-[32px] font-black text-white uppercase tracking-wider drop-shadow-md">Extérieur</h2>
                        </div>
                        <ul class="gold-bullets text-[19px] text-stone-200 leading-snug font-medium">
                            <li>Prélavage actif (Snow Foam)</li>
                            <li>Nettoyage jantes & passages</li>
                            <li>Lavage manuel 2 seaux</li>
                            <li>Décontamination carrosserie</li>
                            <li>Dressing pneumatiques</li>
                        </ul>
                    </div>
                </div>'''

html = re.sub(ext_pattern, ext_replacement, html, flags=re.DOTALL)

# Replace Intérieur Column
int_pattern = r'<div class="flex-1 rounded-2xl p-4 gold-bg-light" style="border-left: 1px solid rgba\(196,165,93,0\.15\); border-right: 1px solid rgba\(196,165,93,0\.15\);">\s*<div class="text-center mb-4">\s*<i class="fa-solid fa-spray-can-sparkles text-\[44px\] text-gold mb-3"></i>\s*<h2 class="text-\[32px\] font-black text-white uppercase tracking-wider">Intérieur</h2>\s*</div>\s*<ul class="gold-bullets text-xl text-stone-300 leading-snug">.*?</ul>\s*</div>'

int_replacement = f'''<div class="flex-1 rounded-2xl p-5 relative overflow-hidden group border border-white/10 shadow-xl" style="background: #09090b;">
                    <img src="data:image/png;base64,{int_b64}" class="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-lighten filter contrast-125 brightness-110 transition-transform duration-1000 group-hover:scale-110">
                    <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-black/50 to-black/90 z-0"></div>
                    <div class="relative z-10">
                        <div class="text-center mb-4">
                            <i class="fa-solid fa-spray-can-sparkles text-[44px] text-gold mb-3 drop-shadow-md"></i>
                            <h2 class="text-[32px] font-black text-white uppercase tracking-wider drop-shadow-md">Intérieur</h2>
                        </div>
                        <ul class="gold-bullets text-[19px] text-stone-200 leading-snug font-medium">
                            <li>Aspiration minutieuse (habitacle)</li>
                            <li>Dégraissage plastiques pinceau</li>
                            <li>Shampoing moquettes & tapis</li>
                            <li>Nettoyage profond (cuir/tissu)</li>
                            <li>Vitres intérieures sans trace</li>
                        </ul>
                    </div>
                </div>'''

html = re.sub(int_pattern, int_replacement, html, flags=re.DOTALL)

# Replace Signature Column
sig_pattern = r'<div class="flex-1 rounded-2xl p-4" style="background: rgba\(168,136,74,0\.10\);">\s*<div class="text-center mb-4 relative">\s*<div class="absolute -top-10 -right-3 bg-gold text-black font-bold py-1 px-3 rounded-full text-\[15px\] transform rotate-12">RECOMMANDÉ</div>\s*<i class="fa-solid fa-crown text-\[44px\] text-gold mb-3"></i>\s*<h2 class="text-\[32px\] font-black gold-gradient-text uppercase tracking-wider">Signature</h2>\s*</div>\s*<ul class="gold-bullets text-xl text-white font-medium leading-snug">.*?</ul>\s*</div>'

sig_replacement = f'''<div class="flex-1 rounded-2xl p-5 relative overflow-hidden group border-2 border-gold/40 shadow-[0_0_30px_rgba(196,165,93,0.3)]" style="background: #09090b;">
                    <img src="data:image/png;base64,{full_b64}" class="absolute inset-0 w-full h-full object-cover opacity-50 mix-blend-lighten filter contrast-125 brightness-110 transition-transform duration-1000 group-hover:scale-110">
                    <div class="absolute inset-0 bg-gradient-to-b from-black/70 via-black/40 to-black/90 z-0"></div>
                    <div class="relative z-10">
                        <div class="text-center mb-4 relative">
                            <div class="absolute -top-6 -right-6 bg-gold text-black font-black py-1 px-4 rounded-lg text-[14px] transform rotate-12 shadow-lg tracking-widest border border-yellow-200">PREMIUM</div>
                            <i class="fa-solid fa-crown text-[44px] text-gold mb-3 drop-shadow-md"></i>
                            <h2 class="text-[32px] font-black text-gold uppercase tracking-wider drop-shadow-md">Signature</h2>
                        </div>
                        <ul class="gold-bullets text-[19px] text-white font-bold leading-snug">
                            <li class="text-gold">Toutes les prestations Intérieur</li>
                            <li class="text-gold">Toutes les prestations Extérieur</li>
                            <li>Cire Brillance Express (3 mois)</li>
                            <li>Soin protecteur anti-UV</li>
                        </ul>
                    </div>
                </div>'''

html = re.sub(sig_pattern, sig_replacement, html, flags=re.DOTALL)


# Main Background - Let's use the full GT3RS image for the main background too!
main_bg_pattern = r'<!-- LUXURY BACKGROUND -->.*?</div>\s*</div>\s*<!-- Début du Flyer -->'
# Wait, the main background was injected in the body or in #flyer-post?
# The bg_update.py injected it into <!-- LUXURY BACKGROUND --> ... </div>
# Let's find it.
# We will just change the base64 of the main background to full_b64, making it a GT3 RS background.
html = re.sub(r'<!-- LUXURY BACKGROUND -->.*?<!-- Éclairage studio', f'''<!-- LUXURY BACKGROUND -->
        <div style="position:absolute; inset:0; z-index:1; overflow:hidden; background: #09090B;">
            <!-- Image de fond GT3 RS -->
            <img src="data:image/png;base64,{full_b64}" style="width:100%; height:100%; object-fit:cover; opacity:0.25; mix-blend-mode: lighten; filter: contrast(120%) brightness(0.9);">
            
            <!-- Éclairage studio''', html, flags=re.DOTALL)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("GT3 RS cards added!")
