import os
import subprocess
import re
import base64
import glob

def get_latest_bg():
    full_images = glob.glob(r"C:\Users\adame\.gemini\antigravity\brain\47f74917-4f43-4e0e-be25-9c4dc8f143a0\gt3rs_full_*.png")
    if not full_images:
        return None
    full_img_path = max(full_images, key=os.path.getctime)
    with open(full_img_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def export_social(width, height, output_name, layout_type="full"):
    with open('flyer_base.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    bg_b64 = get_latest_bg()
    
    # Standard scale based on width
    scale = width / 1748.0
    
    # Extract content
    pattern = r'(<div\s+id="flyer-post"[^>]*>)(.*?)(</div>\s*<!--\s*Fin Flyer\s*-->)'
    match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if not match: return
    content = match.group(2)
    content = re.sub(r'<!-- Background GT3 RS -->.*?<!-- End Background -->', '', content, flags=re.DOTALL)

    # Specific Layout Adjustments
    layout_css = ""
    if layout_type == "square":
        # For square, we hide the big table and focus on cards
        layout_css = """
            .vehicle-table { display: none !important; }
            .content-wrapper { 
                top: 50% !important; 
                transform: scale(0.65) translateY(-60%) !important; 
            }
            .qr-container { transform: scale(1.4) !important; margin-top: 40px; }
        """
    elif layout_type == "portrait":
        layout_css = """
            .content-wrapper { 
                top: 45% !important; 
                transform: scale(0.62) translateY(-50%) !important; 
            }
        """
    elif layout_type == "story":
        layout_css = """
            .content-wrapper { 
                top: 50% !important; 
                transform: scale(0.62) translateY(-55%) !important; 
            }
        """

    social_html = f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: #000; overflow: hidden; }}
            #flyer-post {{
                width: {width}px;
                height: {height}px;
                position: relative;
                overflow: hidden;
                background-color: #050505;
            }}
            .social-bg {{
                position: absolute;
                inset: 0;
                z-index: 0;
            }}
            .social-bg img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                opacity: 0.55;
                filter: brightness(0.5) contrast(1.1) saturate(1.1);
            }}
            .social-overlay {{
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.4) 100%);
                z-index: 1;
            }}
            .content-wrapper {{
                position: absolute;
                z-index: 10;
                width: 1748px;
                height: 2480px;
                transform: scale({scale});
                transform-origin: center center;
                left: 50%;
                margin-left: -874px;
                top: 0;
            }}
            /* Identify the table to hide it in square mode */
            .grid.grid-cols-4.gap-2.mb-12 {{ class: vehicle-table; }}
            {layout_css}
        </style>
        <script>
            window.onload = () => {{
                // Tag the table for CSS targeting
                const tables = document.querySelectorAll('.grid-cols-4');
                tables.forEach(t => t.classList.add('vehicle-table'));
                // Tag QR code for scaling
                const qr = document.querySelector('.bg-black\\\\/40.p-4');
                if(qr) qr.parentElement.classList.add('qr-container');
            }};
        </script>
    </head>
    <body>
        <div id="flyer-post">
            <div class="social-bg">
                <img src="data:image/jpeg;base64,{bg_b64}">
                <div class="social-overlay"></div>
            </div>
            <div class="content-wrapper">
                {content}
            </div>
        </div>
    </body>
    </html>
    '''

    temp_file = f'temp_{output_name}.html'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(social_html)
    
    print(f"Exporting {output_name} ({width}x{height}) - Layout: {layout_type}")
    subprocess.run(['python', 'export.py', '--html', temp_file, '--output', output_name, '--width', str(width), '--height', str(height), '--wait', '3500'])
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    export_social(1080, 1920, 'flyer_story_9_16.png', "story")
    export_social(1080, 1350, 'flyer_post_portrait.png', "portrait")
    export_social(1080, 1080, 'flyer_post_square.png', "square")
    print("\nPremium Social Media Adaptation Complete.")
