"""
Export Flyer PNG pixel-perfect via Playwright.
Remplace html2canvas pour éviter les décalages de rendu.
Usage: python export.py --html flyer.html --output flyer.png --width 1748 --height 2480 --wait 2500
"""
import argparse
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def export_flyer(html_path: str, output_path: str, width: int, height: int, wait_ms: int = 2500):
    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)
    file_url = Path(html_path).as_uri()

    print(f"[Export] HTML : {html_path}")
    print(f"[Export] Output : {output_path}")
    print(f"[Export] Dimensions : {width}x{height}")
    print(f"[Export] Attente fonts : {wait_ms}ms")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(wait_ms)

        # Cibler uniquement le conteneur #flyer-post (pas le body avec le bouton)
        flyer_el = page.query_selector("#flyer-post")
        if flyer_el:
            flyer_el.screenshot(path=output_path, type="png")
            print(f"[Export] Screenshot de #flyer-post sauvegardé.")
        else:
            # Fallback: screenshot de la page entière clippée aux dimensions
            page.screenshot(path=output_path, type="png", clip={
                "x": 0, "y": 0, "width": width, "height": height
            })
            print(f"[Export] Screenshot full-page clippé sauvegardé.")

        browser.close()

    # Vérifier les dimensions
    try:
        from PIL import Image
        img = Image.open(output_path)
        print(f"[Export] Dimensions PNG final : {img.size[0]}x{img.size[1]}")
        if img.size != (width, height):
            print(f"[WARN] Dimensions attendues {width}x{height}, obtenues {img.size[0]}x{img.size[1]}")
        else:
            print(f"[OK] Dimensions correctes !")
        img.close()
    except ImportError:
        print("[INFO] PIL non installé, vérification des dimensions ignorée.")

    print(f"[Export] Terminé : {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export flyer HTML en PNG via Playwright")
    parser.add_argument("--html", required=True, help="Chemin du fichier HTML")
    parser.add_argument("--output", required=True, help="Chemin du fichier PNG de sortie")
    parser.add_argument("--width", type=int, default=1748, help="Largeur en pixels (défaut: 1748)")
    parser.add_argument("--height", type=int, default=2480, help="Hauteur en pixels (défaut: 2480)")
    parser.add_argument("--wait", type=int, default=2500, help="Attente en ms pour le chargement des fonts (défaut: 2500)")
    args = parser.parse_args()

    export_flyer(args.html, args.output, args.width, args.height, args.wait)
