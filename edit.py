import re

with open('flyer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make logo bigger
content = content.replace('h-32 mb-8 object-contain', 'h-48 mb-2 object-contain')

# Reduce header margin slightly to avoid overflow
content = content.replace('<div class="text-center mb-8 flex flex-col items-center">', '<div class="text-center mb-2 flex flex-col items-center">')

# Modify QR code container
content = content.replace('<div class="flex flex-col items-center bg-white p-4 rounded-2xl shadow-[0_0_30px_rgba(255,255,255,0.2)]">', '<div class="flex flex-col items-center justify-center border-l-2 border-gold/30 pl-8 ml-4">')

# Modify QR code img and add branding
qr_replacement = r'alt="QR Code Rendez-vous" class="\1 mb-3" style="filter: invert(1) contrast(1.2); mix-blend-mode: screen;">\n                    <div class="text-gold font-bold tracking-widest uppercase text-xl mt-1 text-center">RÉSERVEZ EN LIGNE</div>\n                    <div class="text-stone-300 font-medium tracking-widest mt-1 text-center text-sm">SCANNEZ LE QR CODE</div>'

content = re.sub(r'alt="QR Code Rendez-vous" class="([^"]+)">', qr_replacement, content)

with open('flyer.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
