from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


# from .models import AuthLog

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
    

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_bookings = 42  # temporary/fake
    active_operators = 5  # temporary/fake

    # Fetch latest 50 authentication logs
    logs = AuthLog.objects.all()[:50]

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'active_operators': active_operators,
        'logs': logs,
    }
    return render(request, 'admin/admin_dashboard.html', context)



                # booking backend


class Booking(models.Model):
    PAYMENT_CHOICES = [
        ('UPI', 'UPI'),
        ('Cash', 'Cash'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    passenger = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    passenger_name = models.CharField(max_length=100)
    zone = models.CharField(max_length=50)
    pickup_location = models.CharField(max_length=100)
    drop_location = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.passenger_name}"
