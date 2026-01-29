from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        import os
        from django.contrib.auth.models import User

        if os.environ.get("CREATE_SUPERUSER") == "true":
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password=os.environ.get("ADMIN_PASSWORD", "changeme123")
                )