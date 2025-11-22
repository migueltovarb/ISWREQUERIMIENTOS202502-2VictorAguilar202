import os
import django
import requests
import random
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from reservations.models import Room
from django.conf import settings

def download_image(filename, keyword="study"):
    # Using picsum for reliable random images, or we could try unsplash source if available
    # picsum.photos/seed/{seed}/800/600 gives a consistent image for a seed
    seed = random.randint(1, 10000)
    url = f"https://picsum.photos/seed/{seed}/800/600"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            save_path = os.path.join(settings.MEDIA_ROOT, 'rooms')
            os.makedirs(save_path, exist_ok=True)
            full_path = os.path.join(save_path, filename)
            
            with open(full_path, 'wb') as f:
                f.write(response.content)
            return f"rooms/{filename}"
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

def assign_stock_images():
    rooms = Room.objects.all()
    for room in rooms:
        filename = f"room_stock_{room.id}.jpg"
        print(f"Downloading image for {room.name}...")
        
        # We use a random seed logic inside download_image to get different images
        image_rel_path = download_image(filename)
        
        if image_rel_path:
            room.image = image_rel_path
            room.save()
            print(f"Assigned {image_rel_path} to {room.name}")
        else:
            print(f"Failed to download image for {room.name}")
        
        # Be nice to the API
        time.sleep(1)

if __name__ == '__main__':
    assign_stock_images()
