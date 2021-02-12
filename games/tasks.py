from celery import shared_task

from django.conf import settings
from datetime import datetime, timezone
from .models import Penalty

@shared_task
def remove_penalty():
    now = datetime.now(timezone.utc)
    for penalty in Penalty.objects.all():
        elapsed_time = (now-penalty.created).seconds
        if elapsed_time > settings.PENALTY_TIMER and penalty.type=='red':
            penalty.delete()
 

