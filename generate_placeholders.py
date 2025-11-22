import os
import django
from PIL import Image, ImageDraw, ImageFont
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from reservations.models import Room
from django.conf import settings

def generate_placeholder(text, filename):
    width, height = 800, 600
    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    img = Image.new('RGB', (width, height), color=color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text position (center)
    # For default font, textbbox might not work as expected in older Pillow, but let's try basic centering
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)
    
    d.text(position, text, fill=(255, 255, 255), font=font)
    
    # Ensure directory exists
    save_path = os.path.join(settings.MEDIA_ROOT, 'rooms')
    os.makedirs(save_path, exist_ok=True)
    
    full_path = os.path.join(save_path, filename)
    img.save(full_path)
    return f"rooms/{filename}"

def assign_images():
    rooms = Room.objects.all()
    for room in rooms:
        if not room.image:
            filename = f"room_{room.id}.jpg"
            print(f"Generating image for {room.name}...")
            image_rel_path = generate_placeholder(room.name, filename)
            room.image = image_rel_path
            room.save()
            print(f"Assigned {image_rel_path} to {room.name}")
        else:
            print(f"Room {room.name} already has an image.")

if __name__ == '__main__':
    assign_images()
