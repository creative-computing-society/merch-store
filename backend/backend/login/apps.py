from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "login"

    def ready(self):
        import login.signals  # Import signals to ensure they are registered