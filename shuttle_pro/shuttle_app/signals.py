from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuthLog
from django.utils.timezone import now

User = get_user_model()

# Track signup
@receiver(post_save, sender=User)
def track_signup(sender, instance, created, **kwargs):
    if created:
        AuthLog.objects.create(user=instance, username=instance.username, event='signup')

# Track login
@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')
    AuthLog.objects.create(user=user, username=user.username, event='login', ip_address=ip, user_agent=ua)

# Track logout
@receiver(user_logged_out)
def track_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')
    AuthLog.objects.create(user=user, username=user.username, event='logout', ip_address=ip, user_agent=ua)

# Track failed login
@receiver(user_login_failed)
def track_failed_login(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')
    AuthLog.objects.create(user=None, username=credentials.get('username',''), event='failed_login', ip_address=ip, user_agent=ua)

# Helper to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
