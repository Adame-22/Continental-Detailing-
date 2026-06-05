import re

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the header and background parts
header_end = html.find('<!-- HEADER / LOGO -->')
if header_end == -1: header_end = html.find('<div class="relative z-10 w-full h-full flex flex-col p-16">')

head_part = html[:header_end]
logo_part = """
        <!-- HEADER / LOGO -->
        <div class="flex justify-center mb-8">
            <div class="p-6 rounded-2xl gold-bg-dark border border-white/5 relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
                <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4MDAgMzAwIj4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ29sZEdyYWRpZW50IiB4MT0iMCIgeTE9IjAiIHgyPSIxIiB5Mj0iMSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiNFNkMyNzkiIC8+CiAgICAgIDxzdG9wIG9mZnNldD0iNTAlIiBzdG9wLWNvbG9yPSIjQzRBNTVEIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiM4QzcxM0QiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJibHVlR3JhZGllbnQiIHgxPSIwIiB5MT0iMCIgeDI9IjEiIHkyPSIxIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzZCQThFNCIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjM0Q2Qjk5IiAvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDxmaWx0ZXIgaWQ9Imdsb3ciPgogICAgICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIyIiByZXN1bHQ9ImNvbG9yZWRCbHVyIi8+CiAgICAgIDxmZU1lcmdlPgogICAgICAgIDxmZU1lcmdlTm9kZSBpbj0iY29sb3JlZEJsdXIiLz4KICAgICAgICA8ZmVNZXJnZU5vZGUgaW49IlNvdXJjZUdyYXBoaWMiLz4KICAgICAgPC9mZU1lcmdlPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIAogIDwhLS0gU2lsaG91ZXR0ZSBkZSBsYSB2b2l0dXJlIC0tPgogIDxwYXRoIGQ9Ik0gMTUwIDE4MCBDIDE4MCAxMzAgMjUwIDEwMCAzNTAgMTAwIEMgNDUwIDEwMCA1MDAgMTEwIDYwMCAxNDAgQyA2NTAgMTYwIDY4MCAxODAgNzAwIDE4MCIgCiAgICAgICAgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2JsdWVHcmFkaWVudCkiIHN0cm9rZS13aWR0aD0iNCIgZmlsdGVyPSJ1cmwoI2dsb3cpIiAvPgogIDxwYXRoIGQ9Ik0gMjAwIDE4MCBDIDIyMCAxNTAgMjgwIDE0MCAzNTAgMTQwIEMgNDIwIDE0MCA0ODAgMTUwIDUwMCAxODAiIAogICAgICAgIGZpbGw9Im5vbmUiIHN0cm9rZT0idXJsKCNnb2xkR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjIiIC8+CiAgCiAgPCEtLSBSb3VlcyAtLT4KICA8Y2lyY2xlIGN4PSIyNTAiIGN5PSIxODAiIHI9IjMwIiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjYmx1ZUdyYWRpZW50KSIgc3Ryb2tlLXdpZHRoPSI0IiAvPgogIDxjaXJjbGUgY3g9IjI1MCIgY3k9IjE4MCIgcj0iMjAiIGZpbGw9Im5vbmUiIHN0cm9rZT0idXJsKCNnb2xkR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjIiIC8+CiAgPGFyYyBjeD0iMjUwIiBjeT0iMTgwIiByPSIxMCIgZmlsbD0idXJsKCNnb2xkR3JhZGllbnQpIiAvPgogIAogIDxjaXJjbGUgY3g9IjU1MCIgY3k9IjE4MCIgcj0iMzAiIGZpbGw9Im5vbmUiIHN0cm9rZT0idXJsKCNibHVlR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjQiIC8+CiAgPGNpcmNsZSBjeD0iNTUwIiBjeT0iMTgwIiByPSIyMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2dvbGRHcmFkaWVudCkiIHN0cm9rZS13aWR0aD0iMiIgLz4KICA8YXJjIGN4PSI1NTAiIGN5PSIxODAiIHI9IjEwIiBmaWxsPSJ1cmwoI2dvbGRHcmFkaWVudCkiIC8+CiAgCiAgPCEtLSBMaWduZXMgbW91dmVtZW50IC0tPgogIDxwYXRoIGQ9Ik0gMTAwIDE4MCBMIDcwIDE4MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2dvbGRHcmFkaWVudCkiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CiAgPHBhdGggZD0iTSAxMjAgMTYwIEwgODAgMTYwIiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjYmx1ZUdyYWRpZW50KSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KICA8cGF0aCBkPSJNIDc1MCAxODAgTCA3ODAgMTgwIiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjZ29sZEdyYWRpZW50KSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KICA8cGF0aCBkPSJNIDcyMCAxNjAgTCA3NjAgMTYwIiBmaWxsPSJub25lIiBzdHJva2U9InVybCgjYmx1ZUdyYWRpZW50KSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KCiAgPCEtLSBUZXh0ZSAtLT4KICA8dGV4dCB4PSI0MDAiIHk9IjI1MCIgZm9udC1mYW1pbHk9IkNpbmNlbCwgUGxheWZhaXIgRGlzcGxheSwgc2VyaWYiIGZvbnQtc2l6ZT0iNTIiIGZvbnQtd2VpZ2h0PSI3MDAiIGZpbGw9InVybCgjYmx1ZUdyYWRpZW50KSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgbGV0dGVyLXNwYWNpbmc9IjRweCI+Q09OVElORU5UQUw8L3RleHQ+CiAgPHRleHQgeD0iNDAwIiB5PSIyOTAiIGZvbnQtZmFtaWx5PSJJbnRlciwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9IjUwMCIgZmlsbD0idXJsKCNnb2xkR3JhZGllbnQpIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBsZXR0ZXItc3BhY2luZz0iMTBweCI+REVUQUlMSU5HPC90ZXh0Pgo8L3N2Zz4=" alt="Continental Detailing" class="w-[320px] drop-shadow-2xl relative z-10">
            </div>
        </div>
"""

new_html = head_part + '''<div class="relative z-10 w-full h-full flex flex-col p-16">''' + logo_part + """
        <!-- TITLE -->
        <div class="text-center mb-16 mt-4">
            <h1 class="text-[75px] font-black text-gold uppercase tracking-widest drop-shadow-lg">NOS TARIFS</h1>
        </div>

        <div class="flex flex-col gap-12 flex-grow">
            <!-- EXTERIEUR -->
            <div class="glass-row rounded-[40px] p-12 border border-white/10 flex items-center" style="box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                <!-- Info -->
                <div class="w-[45%] pr-12 border-r border-white/10">
                    <h2 class="text-[55px] font-black text-white uppercase flex items-center gap-6 mb-8">
                        <i class="fa-solid fa-spray-can text-gold text-[65px]"></i> EXTÉRIEUR
                    </h2>
                    <ul class="text-[34px] text-stone-300 space-y-6 font-medium leading-tight">
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Prélavage Snow Foam</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Lavage manuel 2 seaux</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Décontamination Jantes</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Dressing Pneus brillant</span></li>
                    </ul>
                </div>
                <!-- Prices -->
                <div class="w-[55%] pl-12">
                    <div class="grid grid-cols-2 gap-x-8 gap-y-6 text-[36px] font-bold text-white">
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Citadine</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">49€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Berline</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">59€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">SUV</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">69€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Mono 5pl</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">79€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5 col-span-2"><span class="text-stone-300">Monospace 7 places</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">89€</span></div>
                    </div>
                </div>
            </div>

            <!-- INTERIEUR -->
            <div class="glass-row rounded-[40px] p-12 border border-white/10 flex items-center" style="box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                <!-- Info -->
                <div class="w-[45%] pr-12 border-r border-white/10">
                    <h2 class="text-[55px] font-black text-white uppercase flex items-center gap-6 mb-8">
                        <i class="fa-solid fa-couch text-gold text-[65px]"></i> INTÉRIEUR
                    </h2>
                    <ul class="text-[34px] text-stone-300 space-y-6 font-medium leading-tight">
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Aspiration minutieuse</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Shampoing Tissus</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Plastiques au pinceau</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-check text-gold mt-2 text-[30px]"></i> <span>Soin Cuirs pH neutre</span></li>
                    </ul>
                </div>
                <!-- Prices -->
                <div class="w-[55%] pl-12">
                    <div class="grid grid-cols-2 gap-x-8 gap-y-6 text-[36px] font-bold text-white">
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Citadine</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">79€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Berline</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">89€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">SUV</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">99€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5"><span class="text-stone-300">Mono 5pl</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">109€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-white/5 col-span-2"><span class="text-stone-300">Monospace 7 places</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">119€</span></div>
                    </div>
                </div>
            </div>

            <!-- SIGNATURE -->
            <div class="gold-bg-dark rounded-[40px] p-12 border-2 border-gold/40 flex items-center relative overflow-hidden" style="box-shadow: 0 0 50px rgba(196,165,93,0.2);">
                <div class="absolute top-10 -right-14 bg-gold text-black font-black py-3 px-20 text-[26px] tracking-widest transform rotate-45 shadow-lg">PREMIUM</div>
                <!-- Info -->
                <div class="w-[45%] pr-12 border-r border-gold/30 relative z-10">
                    <h2 class="text-[55px] font-black text-white uppercase flex items-center gap-6 mb-8">
                        <i class="fa-solid fa-crown text-gold text-[65px] drop-shadow-md"></i> SIGNATURE
                    </h2>
                    <ul class="text-[34px] text-white space-y-6 font-medium leading-tight">
                        <li class="flex items-start gap-5"><i class="fa-solid fa-plus text-gold mt-2 text-[30px]"></i> <span>Pack EXTÉRIEUR</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-plus text-gold mt-2 text-[30px]"></i> <span>Pack INTÉRIEUR</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-star text-gold mt-2 text-[30px]"></i> <span>Cire Brillance Express</span></li>
                        <li class="flex items-start gap-5"><i class="fa-solid fa-shield-halved text-gold mt-2 text-[30px]"></i> <span>Soin Protecteur UV</span></li>
                    </ul>
                </div>
                <!-- Prices -->
                <div class="w-[55%] pl-12 relative z-10">
                    <div class="grid grid-cols-2 gap-x-8 gap-y-6 text-[36px] font-bold text-white">
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-gold/20"><span class="text-stone-100">Citadine</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">119€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-gold/20"><span class="text-stone-100">Berline</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">129€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-gold/20"><span class="text-stone-100">SUV</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">139€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-gold/20"><span class="text-stone-100">Mono 5pl</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">149€</span></div>
                        <div class="flex justify-between items-center bg-black/40 px-6 py-5 rounded-2xl border border-gold/20 col-span-2"><span class="text-stone-100">Monospace 7 places</span> <span class="text-[55px] font-black text-gold leading-none drop-shadow-md">159€</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- OPTIONS & UTILITAIRE -->
        <div class="flex gap-12 mt-12 mb-12">
            <div class="w-1/2 p-10 rounded-[32px] bg-black/40 border border-white/5">
                <h3 class="text-[40px] font-black text-white mb-8 uppercase flex items-center gap-4"><i class="fa-solid fa-plus-circle text-gold"></i> OPTIONS</h3>
                <ul class="flex flex-col gap-6 text-[30px] text-stone-300">
                    <li class="flex justify-between items-center"><span class="flex items-center gap-4"><i class="fa-solid fa-paw text-gold w-10"></i> Poils d'animaux</span> <span class="font-bold text-gold bg-gold/10 px-4 py-2 rounded-xl">+20€</span></li>
                    <li class="flex justify-between items-center"><span class="flex items-center gap-4"><i class="fa-solid fa-box-open text-gold w-10"></i> Véhicule non vidé</span> <span class="font-bold text-gold bg-gold/10 px-4 py-2 rounded-xl">+10€</span></li>
                    <li class="flex justify-between items-center"><span class="flex items-center gap-4"><i class="fa-solid fa-shield text-gold w-10"></i> Cire hydrophobe</span> <span class="font-bold text-gold bg-gold/10 px-4 py-2 rounded-xl">+30€</span></li>
                </ul>
            </div>
            
            <div class="w-1/2 p-10 rounded-[32px] bg-black/40 border border-white/5 flex flex-col justify-center items-center text-center">
                <i class="fa-solid fa-truck text-gold text-[70px] mb-4"></i>
                <h3 class="text-[45px] font-black text-white uppercase mb-2">Utilitaires & Pros</h3>
                <p class="text-[28px] text-stone-400 mb-6">Master, Transit, Flottes, VO/VN</p>
                <div class="bg-gold/10 border border-gold/30 text-gold font-black text-[36px] px-8 py-3 rounded-2xl uppercase tracking-widest drop-shadow-md">
                    Sur Devis
                </div>
            </div>
        </div>


        <div class="flex-grow"></div>

        <!-- FOOTER -->
        <div class="mt-auto gold-bg-dark rounded-2xl p-8 flex items-center justify-between border border-gold/20 relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
            
            <div class="flex flex-col gap-6 relative z-10">
                <div class="flex items-center gap-6">
                    <h2 class="text-[46px] font-black text-white tracking-wider"><i class="fa-solid fa-phone text-gold mr-4"></i>+33 7 50 87 59 64</h2>
                </div>
                
                <div class="flex items-center gap-6">
                    <div class="text-[28px] font-bold text-gold tracking-widest"><i class="fa-solid fa-globe text-stone-300 mr-4"></i>continentaldetailing.fr</div>
                </div>

                <div class="flex gap-8 mt-2">
                    <div class="flex items-center gap-3 text-xl text-stone-200"><i class="fa-solid fa-house-chimney text-gold"></i> Service à domicile</div>
                    <div class="flex items-center gap-3 text-xl text-stone-200"><i class="fa-solid fa-location-dot text-gold"></i> Essonne (91) & Seine-et-Marne (77)</div>
                </div>
            </div>

            <!-- QR Code -->
            <div class="relative z-10 flex flex-col items-center bg-[#09090B] p-4 rounded-xl border border-gold/30 shadow-2xl">
                <img src="qrcode.png" alt="QR Code" class="w-[180px] h-[180px] rounded-lg">
                <div class="text-gold font-bold text-sm tracking-widest mt-4 uppercase">SCANNER POUR RÉSERVER</div>
            </div>
        </div>
        
    </div>
</div>
</body>
</html>
"""

with open('flyer_tarifs.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('flyer_tarifs.html created.')

