from django.db.models import signals
from django.contrib.auth.models import User

from .models import Player

def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

