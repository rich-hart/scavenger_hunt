from django.db.models import signals
from django.contrib.auth.models import User

from .models import Profile

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

