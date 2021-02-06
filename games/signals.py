import random
from django.db.models import signals
from django.contrib.auth.models import User

from .models import *

def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(profile=instance)

def reward_player(sender, instance, created, **kwargs):
    if created:
        rewards = Reward.objects.filter(challenge=instance.challenge)
        for reward in rewards:
            awards = Award.objects.filter(reward=reward)
            if awards and reward.unique:
                continue
            award = Award.objects.filter(reward=reward,player=instance.player).first()
            if not award:
                event = random.random()
                if reward.rate > event:
                   Award.objects.create(player=instance.player, reward=reward)
 
 

