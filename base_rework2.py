import re

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rework Header
old_header = r'<div class="inline-block rounded-\[40px\] px-14 py-6 bg-black/50 mb-6" style="border: 2px solid rgba\(196,165,93,0\.35\);">\s*<div class="text-\[50px\] font-black text-white uppercase tracking-widest leading-none mb-3">OFFRE SPÉCIALE SÉNIOR</div>\s*<div class="text-\[65px\] font-black text-gold uppercase tracking-widest leading-none">-35% TOUTE L\'ANNÉE</div>\s*</div>\s*<p class="text-\[26px\] text-stone-200 font-medium tracking-wide mx-auto leading-snug">\s*Nettoyage prestige à domicile\. <strong class="text-white font-bold">Un véhicule comme neuf, sans effort !</strong>\s*</p>'

new_header = """<h2 class="text-[40px] font-bold text-gold uppercase tracking-widest mb-6">Préparation Esthétique Automobile à Domicile</h2>
                <p class="text-[26px] text-stone-200 font-medium tracking-wide mx-auto leading-snug">
                    L'excellence du detailing chez vous. <strong class="text-white font-bold">Un véhicule protégé et sublimé.</strong>
                </p>"""

content = re.sub(old_header, new_header, content)

# 2. Fix Prices
def price_replacer(match):
    old_price = match.group(1)
    classes = match.group(2)
    return f'<div class="w-1/4 text-center flex flex-col items-center justify-center -mt-2"><span class="text-[55px] font-black {classes} leading-none">{old_price}</span></div>'

# Current format in file:
# <div class="w-1/4 text-center"><div class="text-[24px] line-through text-red-400 font-bold">49€</div><div class="text-[55px] font-black text-white leading-none">32€</div></div>

def exact_price_replacer(match):
    original_price = match.group(1)
    classes = match.group(2)
    return f'<div class="w-1/4 text-center"><div class="text-[55px] font-black {classes} leading-none">{original_price}</div></div>'

content = re.sub(r'<div class="w-1/4 text-center"><div class="text-\[24px\] line-through text-red-400 font-bold">(\d+€)</div><div class="text-\[55px\] font-black ([^"]+) leading-none">\d+€</div></div>', exact_price_replacer, content)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
