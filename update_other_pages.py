import os

def update_other_pages(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Section Titles
    content = content.replace('<div class="text-center mb-16 reveal">', '<div class="text-left mb-16 reveal">')
    content = content.replace('text-4xl md:text-5xl font-semibold', 'text-5xl md:text-7xl font-bold tracking-tight')
    content = content.replace('<div class="line-grow h-px mx-auto mt-6"', '<div class="line-grow h-px mt-6"')

    # Footer
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

    # Replace gold accent color with black/primary
    content = content.replace('color:#A8884A;', 'color:#1A1A1E;')
    content = content.replace('border:1px solid rgba(168,136,74,0.3);', 'border:1px solid rgba(0,0,0,0.1);')
    content = content.replace('background:rgba(168,136,74,0.12);', 'background:rgba(0,0,0,0.05);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_other_pages('about.html')
update_other_pages('services.html')
