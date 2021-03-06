from django.apps import AppConfig
from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
class GamesConfig(AppConfig):
    name = 'games'
    def ready(self):
        from games.signals import (
            create_player,
            reward_player,
            add_players,
#            remove_penalty_schedule,
        )
        from users.models import Profile
        from games.models import Achievement, Game
        post_save.connect(receiver=create_player, sender=Profile)
        post_save.connect(receiver=reward_player, sender=Achievement)
        post_save.connect(receiver=add_players, sender=Game)
#        post_migrate.connect(receiver=remove_penalty_schedule, sender=self)
