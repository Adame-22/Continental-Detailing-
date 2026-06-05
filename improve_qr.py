import re

def improve_qr():
    with open('flyer_base.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add CSS animation for pulsing glow if not present
    if '@keyframes qr-glow' not in html:
        style_insertion = r'''
    @keyframes qr-glow {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.05); }
    }
    .qr-pulse {
        animation: qr-glow 3s ease-in-out infinite;
    }
    </style>'''
        html = html.replace('</style>', style_insertion)

    # Pattern for the QR container I just created
    qr_pattern = r'(<!-- QR Code -->\s*<div class="flex flex-col items-center justify-center border-l-2 border-gold/30 pl-8 ml-4">)\s*<div class="relative group">.*?<img src="(data:image/png;base64,[^"]+)" style="width: 160px; height: 160px;">.*?</div>\s*</div>\s*</div>'
    
    # New stylized QR container with pulsing effect
    replacement = r'''\1
                <div class="relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-gold via-yellow-200 to-gold rounded-2xl blur-md qr-pulse"></div>
                    <div class="relative rounded-2xl p-5 flex flex-col items-center justify-center bg-zinc-950 border-2 border-gold/50 shadow-[0_0_25px_rgba(196,165,93,0.2)] transition-all duration-500 group-hover:border-gold group-hover:shadow-[0_0_40px_rgba(196,165,93,0.4)]">
                        <div class="mb-4 text-center">
                            <p class="text-[12px] font-black text-gold/80 uppercase tracking-[0.3em] mb-1">Plateforme de</p>
                            <p class="text-[20px] font-black text-white uppercase tracking-widest leading-none">RÉSERVATION</p>
                        </div>
                        <div class="p-3 bg-white rounded-xl shadow-inner relative overflow-hidden">
                            <div class="absolute inset-0 bg-gradient-to-tr from-gold/10 to-transparent pointer-events-none"></div>
                            <img src="\2" style="width: 150px; height: 150px; display: block;">
                        </div>
                        <div class="mt-3 flex items-center gap-2">
                            <i class="fa-solid fa-mobile-screen-button text-gold text-sm"></i>
                            <span class="text-[11px] font-bold text-stone-400 uppercase tracking-tighter">Disponible 24h/7j</span>
                        </div>
                    </div>
                </div>'''

    new_html = re.sub(qr_pattern, replacement, html, flags=re.DOTALL)
    
    if new_html == html:
        print("Warning: Pattern not found. The container might be different.")

    with open('flyer_base.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("QR Code design pushed to maximum premium level.")

if __name__ == "__main__":
    improve_qr()
