import re

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the GT3 RS background image so the incrustations stand out on a dark background
pattern = r'<!-- Image de fond GT3 RS -->\s*<img src="data:image/png;base64,.*?" style=".*?">'

html = re.sub(pattern, '<!-- Fond sombre uni pour faire ressortir les incrustations -->', html, flags=re.DOTALL)

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fond principal nettoyé !")
