import re

with open('C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/flyer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Enlarge Logo
content = content.replace('h-[340px] mb-1 object-contain', 'h-[380px] mb-2 object-contain')

# 2. Rework Header to massive Senior Banner
old_header = r'<h1 class="text-6xl font-bold text-white uppercase tracking-wider mb-2 mt-\[-10px\]">CONTINENTAL DETAILING</h1>\s*<h2 class="font-serif text-\[2\.75rem\] font-bold gold-gradient-text uppercase tracking-wide leading-tight mb-3">Offre Spéciale Sénior -35% à l\'année</h2>\s*<p class="text-xl text-stone-300 font-light tracking-wide max-w-4xl mx-auto leading-relaxed">\s*Redonnez à votre véhicule son éclat d\'origine sans bouger de chez vous\. <strong class="text-white font-semibold">Excellence, précision et produits haut de gamme\.</strong>\s*</p>'

new_header = '''<h1 class="text-[75px] font-black text-white uppercase tracking-widest mb-4 mt-[-20px] drop-shadow-lg">CONTINENTAL DETAILING</h1>
                <div class="flex flex-col items-center justify-center bg-gradient-to-r from-gold/20 via-gold/40 to-gold/20 border-y-4 border-gold w-full py-4 mb-6 shadow-[0_0_30px_rgba(168,136,74,0.4)]">
                    <h2 class="text-[55px] font-black text-white uppercase tracking-widest leading-none drop-shadow-md mb-2">OFFRE SPÉCIALE SÉNIOR</h2>
                    <div class="text-[65px] font-black text-gold uppercase tracking-widest leading-none drop-shadow-[0_0_20px_rgba(168,136,74,0.8)]">-35% TOUTE L'ANNÉE</div>
                </div>
                <p class="text-[28px] text-stone-200 font-medium tracking-wide max-w-4xl mx-auto leading-snug">
                    Nettoyage prestige à domicile. <strong class="text-white font-bold">Un véhicule comme neuf, sans effort !</strong>
                </p>'''

content = re.sub(old_header, new_header, content)

# 3. Enlarge Services Titles
content = re.sub(r'<h2 class="text-3xl font-bold (text-white|text-gold) uppercase tracking-wider">([^<]+)</h2>', r'<h2 class="text-[36px] font-black \1 uppercase tracking-wider">\2</h2>', content)
content = content.replace('text-4xl text-gold mb-3', 'text-[50px] text-gold mb-3') # Icons

# 4. Enlarge Pricing Headers
content = content.replace('text-2xl font-bold tracking-widest text-stone-400', 'text-[28px] font-black tracking-widest text-stone-300')
content = content.replace('text-2xl font-bold tracking-widest text-gold', 'text-[28px] font-black tracking-widest text-gold')

# 5. Enlarge Vehicle Names
content = re.sub(r'<div class="text-2xl font-bold text-white mb-1">([^<]+)</div>', r'<div class="text-[30px] font-black text-white mb-1 leading-none">\1</div>', content)
content = re.sub(r'<div class="text-lg text-stone-400">([^<]+)</div>', r'<div class="text-[20px] text-stone-300 font-medium leading-none mt-2">\1</div>', content)

# 6. Simplify and Enlarge Prices (Rounding to integers and making them massive)
def price_replacer(match):
    old_price = int(match.group(1))
    classes = match.group(2)
    new_price = round(old_price * 0.65)
    return f'<div class="w-1/4 text-center flex flex-col items-center justify-center -mt-2"><span class="text-[24px] line-through text-red-400 font-bold mb-0">{old_price}€</span><span class="text-[55px] font-black {classes} leading-none">{new_price}€</span></div>'

content = re.sub(r'<div class="w-1/4 text-center flex flex-col items-center justify-center"><span class="text-sm line-through text-stone-400 font-bold">(\d+)€</span><span class="text-3xl ([^"]+) leading-none mt-0\.5">[^<]+</span></div>', price_replacer, content)

# 7. Make "Sur Devis Personnalisé" massive
content = content.replace('text-2xl font-semibold text-gold italic uppercase tracking-widest">Sur Devis Personnalisé', 'text-[36px] font-black text-gold uppercase tracking-widest drop-shadow-md">Sur Devis Personnalisé')

# 8. Reduce paddings aggressively to fit everything within A5 page
content = content.replace('py-4 px-8 glass-row', 'py-2 px-6 glass-row')
content = content.replace('py-4 px-8 border-b-2', 'py-2 px-6 border-b-2')
content = content.replace('py-4 px-8 items-center bg-black/20', 'py-2 px-6 items-center bg-black/20')
content = content.replace('rounded-3xl p-8 gold-bg-light', 'rounded-3xl p-4 gold-bg-light')
content = content.replace('rounded-3xl p-8 backdrop-blur-sm', 'rounded-3xl p-4 backdrop-blur-sm')
content = content.replace('p-6 mb-6 bg-black/50', 'p-4 mb-4 bg-black/50')
content = content.replace('mb-6 gold-bg-light', 'mb-4 gold-bg-light') # Margin below grid

with open('C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/flyer.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
