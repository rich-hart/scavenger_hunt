import random
from django.db.models import signals
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import *

def create_player(sender, instance, created, **kwargs):
    if created:
        player = Player.objects.create(profile=instance)
        for game in Game.objects.all():
            game.players.add(player)

def add_players(sender, instance, created, **kwargs):
    if created:
        for player in Player.objects.all():
            instance.players.add(player)

def reward_player(sender, instance, created, **kwargs):
    if created:
        rewards = Reward.objects.filter(challenge=instance.challenge)
        for reward in rewards:
            awards = Award.objects.filter(reward=reward)
            if awards and reward.unique:
                continue
            awards = Award.objects.filter(
                reward=reward,
                player=instance.player,
            )
            if len(awards)>1:
                #FIXME: why are duplicated being created?
                for i in range(1,len(awards)):
                    awards[i].delete()
            elif not awards:
                event = random.random()
                if reward.rate > event:
                   Award.objects.create(player=instance.player, reward=reward)
 
 
# executes every 10 seconds.
def remove_penalty_schedule(sender, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,                  # we created this above.
        name='Removing penalties',          # simply describes this periodic task.
        task='games.tasks.remove_penalty',  # name of task.
    )
