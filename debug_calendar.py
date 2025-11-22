import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from reservations.models import Reservation
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_calendar():
    print("Checking Reservation model...")
    reservations = Reservation.objects.all().order_by('-date', '-start_time')
    print(f"Found {reservations.count()} reservations.")

    for res in reservations:
        print(f"Reservation: {res}")
        print(f"  Room: {res.room.name}")
        print(f"  User: {res.user.email}")
        try:
            print(f"  Role: {res.user.role_name}")
        except Exception as e:
            print(f"  Error accessing role_name: {e}")
        
        print(f"  Date: {res.date}")
        print(f"  Start: {res.start_time}")
        print(f"  End: {res.end_time}")
        print(f"  Reason: {res.reason}")

if __name__ == '__main__':
    debug_calendar()
