import base64

with open('gt3rs-b64.txt', 'r') as f:
    b64 = f.read()

with open('flyer.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_src = 'src="gt3rs-bg.png"'
new_src = 'src="data:image/png;base64,' + b64 + '"'

html = html.replace(old_src, new_src)

with open('flyer.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Replaced gt3rs-bg.png with base64 data URI')
