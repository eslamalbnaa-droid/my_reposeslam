from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'المتجر'

    def ready(self):
        # Register shop signals when Django loads the app.
        from . import signals  # noqa: F401
