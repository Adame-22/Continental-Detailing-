import os

def update_tailwind_config(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return
    
    # Change Tailwind action color from gold to a dark gray/black for the Porsche DA
    content = content.replace("action: '#A8884A',", "action: '#1A1A1E',")
    content = content.replace("'action-lt': '#C4A55D',", "'action-lt': '#404040',")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_tailwind_config('index.html')
update_tailwind_config('about.html')
update_tailwind_config('services.html')
