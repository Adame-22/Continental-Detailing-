import re

with open('flyer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make logo even bigger
content = content.replace('h-48 mb-2 object-contain', 'h-[280px] mb-4 object-contain')

# Reduce margins of the main blocks to fit the bigger logo
content = content.replace('flex gap-6 mb-10 w-full', 'flex gap-6 mb-6 w-full')
content = content.replace('overflow-hidden mb-10 gold-bg-light', 'overflow-hidden mb-6 gold-bg-light')
content = content.replace('p-6 mb-10 bg-black/50', 'p-6 mb-6 bg-black/50')

with open('flyer.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
