from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthLog(models.Model):
    EVENT_CHOICES = (
        ('signup', 'Signup'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('failed_login', 'Failed Login'),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    username = models.CharField(
        max_length=150, blank=True
    )  # store attempted username for failed logins
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Authentication Log"
        verbose_name_plural = "Authentication Logs"

    def __str__(self):
        display_username = self.username or (self.user.username if self.user else "Anonymous")
        return f"{self.timestamp} — {self.event} — {display_username}"
