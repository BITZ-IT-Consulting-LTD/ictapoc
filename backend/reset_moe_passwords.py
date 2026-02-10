import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from service_api.models import User

def reset_passwords():
    usernames = ['moe_headteacher', 'moe_supervisor', 'moe_printer']
    new_password = 'Starten1@'
    
    for username in usernames:
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            print(f"Password for {username} updated successfully.")
        except User.DoesNotExist:
            print(f"User {username} not found.")

if __name__ == "__main__":
    reset_passwords()
