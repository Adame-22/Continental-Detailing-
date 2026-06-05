import os

def update_css_colors(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return
    
    # Change gold color to black/dark gray
    content = content.replace('#A8884A', '#1A1A1E')
    content = content.replace('#C4A55D', '#404040')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_css_colors('css/style.css')
