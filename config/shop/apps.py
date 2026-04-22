from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        import os
        from django.contrib.auth.models import User
        from django.conf import settings

        if os.environ.get("CREATE_SUPERUSER", "false").lower() == "true":

            username = settings.ADMIN_USERNAME
            email = settings.ADMIN_EMAIL
            password = settings.ADMIN_PASSWORD

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )