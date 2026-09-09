from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'حسابات المستخدمين'

    def ready(self):
        # Register account signals when Django loads the app.
        from . import signals  # noqa: F401
