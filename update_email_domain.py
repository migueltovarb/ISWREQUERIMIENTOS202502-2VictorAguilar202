import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_rooms.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def update_emails():
    users = User.objects.all()
    count = 0
    for user in users:
        if '@university.edu' in user.email:
            old_email = user.email
            new_email = user.email.replace('@university.edu', '@campusucc.edu.co')
            user.email = new_email
            user.save()
            print(f"Updated {old_email} -> {new_email}")
            count += 1
    print(f"Total users updated: {count}")

if __name__ == '__main__':
    update_emails()
