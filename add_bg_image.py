import base64
import glob
import os
import re

def add_background():
    # Find the latest full car image
    full_images = glob.glob(r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\gt3rs_full_*.png")
    if not full_images:
        print("Error: No full car image found.")
        return
    
    full_img_path = max(full_images, key=os.path.getctime)
    with open(full_img_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode('utf-8')

    with open('flyer_base.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Final balance: Car is very visible, but text remains the priority
    bg_html = f'''
        <!-- Background GT3 RS -->
        <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none bg-black">
            <img src="data:image/jpeg;base64,{b64_data}" class="w-full h-full object-cover opacity-100 filter brightness-[0.45] saturate-[1.2] contrast-[1.1]">
            <div class="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/60"></div>
            <div class="absolute inset-0 bg-black/20"></div>
        </div>
    '''

    # Pattern to find the start of #flyer-post
    insertion_point = r'(<div id="flyer-post"[^>]*>)'
    
    if '<!-- Background GT3 RS -->' in html:
        # If already exists, replace it
        print("Replacing existing background with final balanced version...")
        html = re.sub(r'<!-- Background GT3 RS -->.*?<!-- End Background -->', bg_html + '<!-- End Background -->', html, flags=re.DOTALL)
    else:
        # Insert after the opening tag of #flyer-post
        html = re.sub(insertion_point, r'\1' + bg_html + '<!-- End Background -->', html, count=1)

    with open('flyer_base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("GT3 RS background finalized.")

if __name__ == "__main__":
    add_background()
