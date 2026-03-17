import os

files = ['C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/index.html',
         'C:/Users/adame/.gemini/antigravity/scratch/continental-detailing/services.html']

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update old rgba shadow colors to match new gold (#D4A373 -> 212, 163, 115)
    content = content.replace('rgba(212,175,55,', 'rgba(212,163,115,')
    content = content.replace('rgba(212, 175, 55,', 'rgba(212, 163, 115,')
    
    # 2. UX: Make buttons chunkier
    content = content.replace('px-6 py-2.5 rounded-full', 'px-8 py-3 rounded-full text-base')
    content = content.replace('p-5 rounded-3xl', 'p-6 md:p-8 rounded-3xl cursor-pointer hover:shadow-[0_10px_30px_rgba(212,163,115,0.15)] transform hover:-translate-y-1')
    content = content.replace('p-6 rounded-3xl', 'p-6 md:p-8 rounded-3xl cursor-pointer hover:shadow-[0_10px_30px_rgba(212,163,115,0.15)] transform hover:-translate-y-1')
    
    # 3. Increase grid gap for less friction/clutter
    content = content.replace('gap-4', 'gap-6')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('UX and UI refinements applied successfully!')
