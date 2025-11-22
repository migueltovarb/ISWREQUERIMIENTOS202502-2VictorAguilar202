import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from reservations.models import Room

def populate():
    rooms_data = [
        {
            'name': 'Sala de Innovación',
            'capacity': 8,
            'location': 'Edificio de Ingeniería, Piso 3',
            'equipment': 'Pizarra inteligente, Proyector 4K, Mesa de conferencias, 8 Sillas ergonómicas, Conexiones HDMI/USB-C'
        },
        {
            'name': 'Laboratorio de Cómputo A',
            'capacity': 20,
            'location': 'Biblioteca Central, Sótano',
            'equipment': '20 Estaciones de trabajo (i7, 32GB RAM), Proyector, Pizarra blanca, Aire acondicionado'
        },
        {
            'name': 'Sala de Lectura Silenciosa',
            'capacity': 4,
            'location': 'Biblioteca Central, Piso 2',
            'equipment': '4 Sillones de lectura, Iluminación cálida, Mesas individuales, Enchufes para laptop'
        },
        {
            'name': 'Sala de Grupo Pequeño',
            'capacity': 3,
            'location': 'Edificio de Ciencias, Aula 101',
            'equipment': 'Mesa redonda, 3 Sillas, Pizarra pequeña'
        }
    ]

    for data in rooms_data:
        room, created = Room.objects.get_or_create(name=data['name'], defaults=data)
        if created:
            print(f"Created room: {room.name}")
        else:
            print(f"Room already exists: {room.name}")

if __name__ == '__main__':
    populate()
