import os

def update_mega_menu(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return
    
    start_tag = '<!-- Visual Column -->'
    end_tag = '</div>\n        </div>\n    </div>'
    
    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        # Handle the split carefully since '</div>\n        </div>\n    </div>' might appear multiple times or not exactly like this.
        # Let's use a regex or just specific replacement.
        
        # It's safer to just replace the known block
        old_block = '''<!-- Visual Column -->
            <div class="hidden md:flex w-5/12 bg-[#F4F4F4] relative flex-col justify-end p-12">
                <img src="images/car-prestige.png" alt="Continental Detailing Signature" class="absolute inset-0 w-full h-full object-cover mix-blend-multiply opacity-80">
                <div class="absolute inset-0 bg-gradient-to-t from-[#F4F4F4] via-transparent to-transparent opacity-90"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex px-3 py-1 bg-white rounded-full text-[10px] font-bold tracking-[0.15em] uppercase text-primary mb-4 shadow-sm">
                        Signature Luxe
                    </div>
                    <h3 class="text-3xl font-medium text-primary mb-3">Continental Detailing</h3>
                    <p class="text-sm text-secondary leading-relaxed font-light">L'excellence du detailing automobile en Île-de-France. Une finition impeccable, sans compromis.</p>
                </div>
            </div>'''
            
        new_block = '''<!-- Vehicules / Prestations Column (Porsche style) -->
            <div class="hidden md:block w-5/12 bg-[#F4F4F4] overflow-y-auto" style="border-left:1px solid rgba(0,0,0,0.05); max-height: 100vh;">
                <div class="p-8 md:p-12 flex flex-col gap-12">
                    
                    <a href="services.html" class="group block text-center decoration-transparent">
                        <div class="text-left mb-2">
                            <h4 class="text-2xl font-light text-primary">Citadine</h4>
                        </div>
                        <div class="relative mb-3 flex justify-center">
                            <img src="images/car-citadine.png" alt="Citadine" class="w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-105" style="max-height: 140px; transform-origin: bottom center;">
                        </div>
                        <div class="text-left">
                            <span class="inline-block bg-white text-primary text-[11px] font-medium px-4 py-1.5 rounded-full shadow-sm border border-gray-100">À partir de 49€</span>
                        </div>
                    </a>

                    <a href="services.html" class="group block text-center decoration-transparent">
                        <div class="text-left mb-2">
                            <h4 class="text-2xl font-light text-primary">Berline</h4>
                        </div>
                        <div class="relative mb-3 flex justify-center">
                            <img src="images/car-berline.png" alt="Berline" class="w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-105" style="max-height: 140px; transform-origin: bottom center;">
                        </div>
                        <div class="text-left">
                            <span class="inline-block bg-white text-primary text-[11px] font-medium px-4 py-1.5 rounded-full shadow-sm border border-gray-100">À partir de 59€</span>
                        </div>
                    </a>

                    <a href="services.html" class="group block text-center decoration-transparent">
                        <div class="text-left mb-2">
                            <h4 class="text-2xl font-light text-primary">SUV</h4>
                        </div>
                        <div class="relative mb-3 flex justify-center">
                            <img src="images/car-suv.png" alt="SUV" class="w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-105" style="max-height: 140px; transform-origin: bottom center;">
                        </div>
                        <div class="text-left">
                            <span class="inline-block bg-white text-primary text-[11px] font-medium px-4 py-1.5 rounded-full shadow-sm border border-gray-100">À partir de 69€</span>
                        </div>
                    </a>

                    <a href="services.html" class="group block text-center decoration-transparent">
                        <div class="text-left mb-2">
                            <h4 class="text-2xl font-light text-primary">Prestige / Sport</h4>
                        </div>
                        <div class="relative mb-3 flex justify-center">
                            <img src="images/car-prestige.png" alt="Prestige" class="w-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-105" style="max-height: 140px; transform-origin: bottom center;">
                        </div>
                        <div class="text-left">
                            <span class="inline-block bg-white text-primary text-[11px] font-medium px-4 py-1.5 rounded-full shadow-sm border border-gray-100">À partir de 89€</span>
                        </div>
                    </a>

                </div>
            </div>'''
        
        content = content.replace(old_block, new_block)
        
        # Adjust the Links Column to be vertically scrollable too just in case
        content = content.replace('flex-1 p-6 md:p-12 lg:p-20 flex flex-col justify-start bg-white relative z-10', 'flex-1 p-6 md:p-12 lg:p-20 flex flex-col justify-start bg-white relative z-10 overflow-y-auto')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

update_mega_menu('index.html')
update_mega_menu('about.html')
update_mega_menu('services.html')
