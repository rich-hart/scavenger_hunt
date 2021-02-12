from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
import importlib
import pkgutil
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#s3-backend-settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hunt.settings')

app = Celery('hunt')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


#@app.on_after_finalize.connect
#def initiate_procedure(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
#    signature = app.signature('procedures.tasks.initiate') 
#    sender.add_periodic_task(10.0, signature, name='Initiate default procedure')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#app.conf.beat_schedule = {
#    'add-every-30-seconds': {
#        'task': 'procedures.tasks.initiate',
#        'schedule': 10.0,
#        'args': (16, 16)
#    },
#}
app.conf.timezone = 'UTC'


def get_task_plugins():
    task_plugins = {
        finder.path : importlib.import_module(finder.path+name)
        for finder, name, ispkg in pkgutil.iter_modules(settings.INSTALLED_APPS,'.')
          if 'tasks' in name
    }
#    task_plugins = {k:v for k, v in task_plugins.items()}
    return task_plugins

