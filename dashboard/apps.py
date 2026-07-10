from django.apps import AppConfig
from django.db.models.signals import post_migrate

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from .views import auto_create_admin
        post_migrate.connect(auto_create_admin)
