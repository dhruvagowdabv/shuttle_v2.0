"""
WSGI config for shuttle_pro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shuttle_pro.settings')

application = get_wsgi_application()





from django.contrib.auth.models import User
from django.core.management import call_command

try:
    # Run migrations first to ensure the tables exist
    call_command("migrate", interactive=False)

    # List of admins to create
    admins = [
        {"username": "admin", "email": "admin@example.com", "password": "Admin@123"},
        {"username": "meghna", "email": "meghna@gmail.com", "password": "6366"},
        {"username": "dhruva", "email": "dhruva@gmail.com", "password": "8904"},
    ]

    # Loop through and create if not exists
    for admin in admins:
        if not User.objects.filter(username=admin["username"]).exists():
            User.objects.create_superuser(
                username=admin["username"],
                email=admin["email"],
                password=admin["password"]
            )
            print(f"✅ Superuser '{admin['username']}' created successfully.")
        else:
            print(f"ℹ️ Superuser '{admin['username']}' already exists.")

except Exception as e:
    print("⚠️ Superuser creation skipped due to:", e)
