from django.apps import AppConfig

class ShuttleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shuttle_app'

    def ready(self):
        import shuttle_app.signals  # ensures signals are registered
