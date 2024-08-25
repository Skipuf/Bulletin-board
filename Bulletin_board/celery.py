import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bulletin_board.settings')

app = Celery('Bulletin_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'clear_accounts_every_minute': {
        'task': 'accounts.tasks.clear_old',
        'schedule': crontab(),
    },
}
