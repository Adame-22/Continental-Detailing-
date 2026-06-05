import re

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rework Header
old_header = r'<h2 class="text-\[55px\] font-black text-white uppercase tracking-widest leading-none drop-shadow-md mb-2">OFFRE SPÉCIALE SÉNIOR</h2>\s*<div class="text-\[65px\] font-black text-gold uppercase tracking-widest leading-none drop-shadow-\[0_0_20px_rgba\(168,136,74,0\.8\)\]">-35% TOUTE L\'ANNÉE</div>'

new_header = '''<h2 class="text-[55px] font-black text-white uppercase tracking-widest leading-none drop-shadow-md mb-2">PRÉPARATION ESTHÉTIQUE</h2>
                    <div class="text-[60px] font-black text-gold uppercase tracking-widest leading-none drop-shadow-[0_0_20px_rgba(168,136,74,0.8)]">AUTOMOBILE À DOMICILE</div>'''

content = re.sub(old_header, new_header, content)

# 2. Fix Prices
def price_replacer(match):
    old_price = match.group(1)
    classes = match.group(2)
    return f'<div class="w-1/4 text-center flex flex-col items-center justify-center -mt-2"><span class="text-[55px] font-black {classes} leading-none">{old_price}</span></div>'

content = re.sub(r'<div class="w-1/4 text-center flex flex-col items-center justify-center -mt-2"><span class="text-\[24px\] line-through text-red-400 font-bold mb-0">(\d+€)</span><span class="text-\[55px\] font-black ([^"]+) leading-none">\d+€</span></div>', price_replacer, content)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
