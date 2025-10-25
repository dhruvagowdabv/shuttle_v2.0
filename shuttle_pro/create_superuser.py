import os
import django

# Set your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shuttle_pro.settings")
django.setup()

from django.contrib.auth.models import User

# Superuser credentials
USERNAME = "meghna123"
EMAIL = "meghna@gmail.com"
PASSWORD = "meghna123"  # choose a strong password

# Only create if it doesn't exist
if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("✅ Superuser created!")
else:
    print("ℹ️ Superuser already exists.")
