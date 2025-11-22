import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

def create_professor():
    # Create Group
    group, created = Group.objects.get_or_create(name='Profesor')
    if created:
        print("Group 'Profesor' created.")
    else:
        print("Group 'Profesor' already exists.")

    # Create User
    email = 'professor@university.edu'
    password = 'professorpassword123'
    
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(username='professor', email=email, password=password)
        user.groups.add(group)
        print(f"Professor created.\nEmail: {email}\nPassword: {password}")
    else:
        print(f"Professor already exists: {email}")
        user = User.objects.get(email=email)
        if not user.groups.filter(name='Profesor').exists():
            user.groups.add(group)
            print("Added existing user to 'Profesor' group.")

if __name__ == '__main__':
    create_professor()
