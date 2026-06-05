import os

def update_porsche_da(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Hero Section (Left-aligned, massive, white text)
    content = content.replace('<div class="relative z-10 max-w-5xl mx-auto px-6 text-center">', '<div class="relative z-10 max-w-7xl mx-auto px-6 text-left">')
    
    old_hero_btn = 'style="background:#A8884A; color:#F9F9F9; border-radius:9999px; letter-spacing:0.1em;"'
    new_hero_btn = 'style="background:rgba(255,255,255,0.15); backdrop-filter:blur(8px); border:1px solid rgba(255,255,255,0.3); color:#FFFFFF; border-radius:9999px;"'
    content = content.replace(old_hero_btn, new_hero_btn)
    
    old_hero_btn2 = 'style="border:1px solid rgba(255,255,255,0.12); border-radius:9999px; color:var(--muted);"'
    new_hero_btn2 = 'style="border:1px solid rgba(255,255,255,0.3); border-radius:9999px; color:#FFFFFF;"'
    content = content.replace(old_hero_btn2, new_hero_btn2)
    
    content = content.replace('text-5xl md:text-7xl lg:text-8xl font-semibold leading-[1.05] mb-6 text-primary', 'text-6xl md:text-8xl lg:text-[100px] font-bold leading-none mb-6 text-white tracking-tight')
    content = content.replace('<em class="not-italic shimmer-text" style="background-image:linear-gradient(90deg, #A8884A, #DFC47A, #C4A55D, #8B6F37, #C4A55D); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">pour votre voiture.</em>', '<span class="text-white">pour votre voiture.</span>')
    content = content.replace('justify-center', 'justify-start')

    # 2. Section Titles
    content = content.replace('<div class="text-center mb-16 reveal">', '<div class="text-left mb-16 reveal">')
    content = content.replace('text-4xl md:text-5xl font-semibold', 'text-5xl md:text-7xl font-bold tracking-tight')
    content = content.replace('<div class="line-grow h-px mx-auto mt-6"', '<div class="line-grow h-px mt-6"')

    # 3. Cards (Galerie) - add the -> button
    gallery_btn = '<div class="absolute bottom-8 right-8 w-12 h-12 rounded-full bg-black/60 backdrop-blur-md flex items-center justify-center text-white border border-white/10 hover:bg-black transition-colors duration-300"><i class="fa-solid fa-arrow-right"></i></div>'
    content = content.replace('</p>\n                    </div>\n                </div>\n\n                <!-- Secondary items', f'</p>\n                    </div>\n                    {gallery_btn}\n                </div>\n\n                <!-- Secondary items')
    content = content.replace('</p>\n                        </div>\n                    </div>\n                    <div class="h-full', f'</p>\n                        </div>\n                        {gallery_btn}\n                    </div>\n                    <div class="h-full')
    content = content.replace('</p>\n                        </div>\n                    </div>\n                </div>', f'</p>\n                        </div>\n                        {gallery_btn}\n                    </div>\n                </div>')

    # Remove the gold borders from "Nos Formules" icons
    content = content.replace('border:1px solid rgba(168,136,74,0.25); border-radius:9999px; background: rgba(168,136,74,0.05);', 'border:1px solid rgba(0,0,0,0.1); border-radius:12px; background: #F9F9F9;')
    content = content.replace('color:#A8884A;', 'color:#1A1A1E;')
    
    # 4. Footer
    old_footer = '<footer style="border-top:1px solid rgba(255,255,255,0.05);">'
    new_footer = '''<footer class="bg-black pt-16 pb-8" style="border-top:1px solid rgba(255,255,255,0.05);">
        <div class="max-w-5xl mx-auto px-6 flex flex-col items-center mb-16">
            <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="text-white flex flex-col items-center gap-2 hover:text-gray-300 transition-colors bg-transparent border-none cursor-pointer">
                <i class="fa-solid fa-arrow-up text-lg"></i>
                <span class="text-xs tracking-wider">Haut de page</span>
            </button>
        </div>'''
    content = content.replace(old_footer, new_footer)
    
    content = content.replace('color:var(--muted);', 'color:#A0A0A0;')
    content = content.replace("this.style.color='#A8884A'", "this.style.color='#FFFFFF'")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_porsche_da('index.html')
