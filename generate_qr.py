import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont
import os

# URL du site
URL = "https://continental-detailing.vercel.app"

# Couleurs du logo
GOLD = (201, 168, 76)
GOLD_LIGHT = (223, 192, 104)
NAVY = (15, 23, 42)
WHITE = (248, 250, 252)

# 1. Générer le QR code avec style
qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=3,
)
qr.add_data(URL)
qr.make(fit=True)

qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=RadialGradiantColorMask(
        back_color=NAVY,
        center_color=GOLD_LIGHT,
        edge_color=GOLD
    )
)

qr_img = qr_img.convert("RGBA")
qr_size = qr_img.size[0]

# 2. Canvas final
padding_top = 40
padding_bottom = 100
padding_side = 50
canvas_w = qr_size + padding_side * 2
canvas_h = qr_size + padding_top + padding_bottom

canvas = Image.new("RGBA", (canvas_w, canvas_h), NAVY)
draw = ImageDraw.Draw(canvas)

# Bordure dorée
border_margin = 15
draw.rounded_rectangle(
    [border_margin, border_margin, canvas_w - border_margin, canvas_h - border_margin],
    radius=30, outline=GOLD, width=3
)
inner_margin = 22
draw.rounded_rectangle(
    [inner_margin, inner_margin, canvas_w - inner_margin, canvas_h - inner_margin],
    radius=25, outline=(*GOLD, 80), width=1
)

# Coller le QR
qr_x = padding_side
qr_y = padding_top
canvas.paste(qr_img, (qr_x, qr_y))

# 3. Logo au centre
logo_path = os.path.join(os.path.dirname(__file__), "images", "logo_continental.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo_max = int(qr_size * 0.25)
    logo.thumbnail((logo_max, logo_max), Image.LANCZOS)
    
    logo_bg_size = max(logo.size[0], logo.size[1]) + 20
    logo_bg = Image.new("RGBA", (logo_bg_size, logo_bg_size), (0, 0, 0, 0))
    logo_bg_draw = ImageDraw.Draw(logo_bg)
    logo_bg_draw.rounded_rectangle(
        [0, 0, logo_bg_size - 1, logo_bg_size - 1],
        radius=15, fill=NAVY, outline=GOLD, width=2
    )
    lx = (logo_bg_size - logo.size[0]) // 2
    ly = (logo_bg_size - logo.size[1]) // 2
    logo_bg.paste(logo, (lx, ly), logo)
    
    center_x = qr_x + (qr_size - logo_bg_size) // 2
    center_y = qr_y + (qr_size - logo_bg_size) // 2
    canvas.paste(logo_bg, (center_x, center_y), logo_bg)

# 4. Textes
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

text_y = qr_y + qr_size + 15
title = "CONTINENTAL DETAILING"
bbox = draw.textbbox((0, 0), title, font=font_title)
tw = bbox[2] - bbox[0]
draw.text(((canvas_w - tw) // 2, text_y), title, fill=GOLD, font=font_title)

subtitle = "Scannez pour visiter notre site"
bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
sw = bbox2[2] - bbox2[0]
draw.text(((canvas_w - sw) // 2, text_y + 38), subtitle, fill=(*WHITE[:3], 180), font=font_sub)

# 5. Coins déco
corner_len = 20
corner_w = 2
for cx, cy, dx, dy in [
    (border_margin+5, border_margin+5, 1, 1),
    (canvas_w-border_margin-5, border_margin+5, -1, 1),
    (border_margin+5, canvas_h-border_margin-5, 1, -1),
    (canvas_w-border_margin-5, canvas_h-border_margin-5, -1, -1)
]:
    draw.line([(cx, cy), (cx + corner_len*dx, cy)], fill=GOLD_LIGHT, width=corner_w)
    draw.line([(cx, cy), (cx, cy + corner_len*dy)], fill=GOLD_LIGHT, width=corner_w)

# Sauvegarder
output = os.path.join(os.path.dirname(__file__), "images", "qr-code-continental.png")
canvas.convert("RGB").save(output, quality=95)
print(f"QR code genere : {output}")
print(f"Taille : {canvas_w}x{canvas_h}px")
