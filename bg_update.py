import re
import base64

img_path = r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\luxury_car_paint_bg_1778784401456.png"

with open(img_path, "rb") as f:
    bg_b64 = base64.b64encode(f.read()).decode('utf-8')

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacement du bloc GT3 RS
bg_html = f'''<!-- LUXURY BACKGROUND -->
        <div style="position:absolute; inset:0; z-index:1; overflow:hidden; background: #09090B;">
            <!-- Image de fond -->
            <img src="data:image/png;base64,{bg_b64}" style="width:100%; height:100%; object-fit:cover; opacity:0.25; mix-blend-mode: lighten; filter: contrast(120%) brightness(0.9);">
            
            <!-- Éclairage studio doré (Glows) pour donner du relief -->
            <div style="position:absolute; top:-10%; left:20%; width:60%; height:50%; background: radial-gradient(circle, rgba(196,165,93,0.25) 0%, transparent 70%); filter: blur(100px);"></div>
            <div style="position:absolute; bottom:0%; right:-10%; width:50%; height:50%; background: radial-gradient(circle, rgba(196,165,93,0.15) 0%, transparent 70%); filter: blur(100px);"></div>
            <div style="position:absolute; bottom:-10%; left:-10%; width:40%; height:40%; background: radial-gradient(circle, rgba(196,165,93,0.1) 0%, transparent 70%); filter: blur(100px);"></div>
        </div>'''

content = re.sub(r'<!-- GT3 RS Background -->.*?</div>', bg_html, content, flags=re.DOTALL)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Background updated.")
