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





# for superuser
# --- Auto-create superuser on first deploy ---
import os
from django.contrib.auth.models import User
from django.core.management import call_command

try:
    # Run migrations (ensures auth_user table exists)
    call_command("migrate", interactive=False)

    # Create default superuser if it doesn't exist
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Admin@123"
        )
        print("✅ Superuser created: username='admin', password='Admin@123'")
    else:
        print("✅ Superuser already exists.")
except Exception as e:
    print("⚠️ Superuser creation skipped due to:", e)
