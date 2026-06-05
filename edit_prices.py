import re

with open('flyer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make logo even bigger
content = content.replace('h-[280px] mb-4 object-contain', 'h-[340px] mb-1 object-contain')

def replacer(match):
    classes = match.group(1)
    old_price = int(match.group(2))
    new_price = old_price * 0.65
    new_price_str = f"{new_price:.2f}".replace('.', ',') + "€"
    
    return f'<div class="w-1/4 text-center flex flex-col items-center justify-center"><span class="text-sm line-through text-stone-400 font-bold">{old_price}€</span><span class="text-3xl {classes} leading-none mt-0.5">{new_price_str}</span></div>'

content = re.sub(r'<div class="w-1/4 text-center text-3xl ([^"]+)">(\d+)€</div>', replacer, content)

with open('flyer.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
