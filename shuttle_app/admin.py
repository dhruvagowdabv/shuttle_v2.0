
from django.contrib import admin
from .models import AuthLog

@admin.register(AuthLog)
class AuthLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'username', 'event', 'ip_address', 'user_agent')
    list_filter = ('event', 'timestamp')
    search_fields = ('username', 'ip_address', 'user_agent')
