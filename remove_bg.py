from PIL import Image
import os

def remove_white_bg(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    data = img.getdata()
    
    new_data = []
    # threshold for white
    threshold = 240
    for item in data:
        # If it's close to pure white, make it transparent
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(image_path, "PNG")

images = ['images/car-citadine.png', 'images/car-berline.png', 'images/car-suv.png', 'images/car-prestige.png']
for img in images:
    if os.path.exists(img):
        remove_white_bg(img)
        print(f"Removed background for {img}")
