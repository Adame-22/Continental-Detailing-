import re

with open('C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/flyer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the header banner (remove rectangle, make it a pill, remove negative top margin)
old_banner = r'<h1 class="text-\[75px\] font-black text-white uppercase tracking-widest mb-4 mt-\[-20px\] drop-shadow-lg">CONTINENTAL DETAILING</h1>\s*<div class="flex flex-col items-center justify-center bg-gradient-to-r from-gold/20 via-gold/40 to-gold/20 border-y-4 border-gold w-full py-4 mb-6 shadow-\[0_0_30px_rgba\(168,136,74,0\.4\)\]">\s*<h2 class="text-\[55px\] font-black text-white uppercase tracking-widest leading-none drop-shadow-md mb-2">OFFRE SPÉCIALE SÉNIOR</h2>\s*<div class="text-\[65px\] font-black text-gold uppercase tracking-widest leading-none drop-shadow-\[0_0_20px_rgba\(168,136,74,0\.8\)\]">-35% TOUTE L\'ANNÉE</div>\s*</div>'

new_banner = '''<h1 class="text-[75px] font-black text-white uppercase tracking-widest mb-6 drop-shadow-lg leading-none">CONTINENTAL DETAILING</h1>
                <div class="inline-block gold-border rounded-[40px] px-12 py-4 bg-black/60 mb-6 shadow-[0_0_30px_rgba(168,136,74,0.4)]">
                    <div class="text-[40px] font-black text-white uppercase tracking-widest leading-none mb-2">OFFRE SPÉCIALE SÉNIOR</div>
                    <div class="text-[50px] font-black text-gold uppercase tracking-widest leading-none">-35% TOUTE L'ANNÉE</div>
                </div>'''

content = re.sub(old_banner, new_banner, content)

# Fix the pricing alignment (remove -mt-2 and adjust sizes to align properly)
def price_fixer(match):
    old_price = match.group(1)
    classes = match.group(2)
    new_price = match.group(3)
    return f'<div class="w-1/4 text-center flex flex-col items-center justify-center"><span class="text-[20px] line-through text-red-400 font-bold mb-1">{old_price}€</span><span class="text-[48px] font-black {classes} leading-none">{new_price}€</span></div>'

content = re.sub(r'<div class="w-1/4 text-center flex flex-col items-center justify-center -mt-2"><span class="text-\[24px\] line-through text-red-400 font-bold mb-0">(\d+)€</span><span class="text-\[55px\] font-black ([^ ]+) leading-none">(\d+)€</span></div>', price_fixer, content)

# Make sure "Sur Devis Personnalisé" is not causing overflow
content = content.replace('text-[36px] font-black text-gold uppercase tracking-widest drop-shadow-md">Sur Devis Personnalisé', 'text-[32px] font-black text-gold uppercase tracking-widest drop-shadow-md mt-2">Sur Devis Personnalisé')


with open('C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/flyer.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
