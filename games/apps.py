from django.apps import AppConfig
from django.db.models.signals import post_save

class GamesConfig(AppConfig):
    name = 'games'
    def ready(self):
        from games.signals import create_player
        from users.models import Profile
        post_save.connect(receiver=create_player, sender=Profile)

