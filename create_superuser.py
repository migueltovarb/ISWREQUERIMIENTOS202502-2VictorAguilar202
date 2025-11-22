import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = 'admin@university.edu'
password = 'adminpassword123'

if not User.objects.filter(email=email).exists():
    # username is required by AbstractUser but we use email as USERNAME_FIELD
    # We still need to provide a username because it's in REQUIRED_FIELDS
    User.objects.create_superuser(username='admin', email=email, password=password)
    print(f"Superuser created.\nEmail: {email}\nPassword: {password}")
else:
    print(f"Superuser already exists.\nEmail: {email}\nPassword: {password}")
