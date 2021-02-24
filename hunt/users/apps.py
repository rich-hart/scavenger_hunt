from django.apps import AppConfig
from django.db.models.signals import post_save

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from users.signals import create_profile
        from django.contrib.auth.models import User
        post_save.connect(receiver=create_profile, sender=User)
