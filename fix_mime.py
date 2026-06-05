import re

with open('flyer_base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace incorrect PNG mime type with JPEG mime type if the base64 string starts with /9j/
html = html.replace('data:image/png;base64,/9j/', 'data:image/jpeg;base64,/9j/')

with open('flyer_base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("MIME types fixed!")
