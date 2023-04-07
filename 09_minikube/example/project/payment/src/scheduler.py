import socket
from celery import Celery

app = Celery(broker='redis://payment-redis-leader:6379/0',
             backend='redis://payment-redis-leader:6379/1')

app.conf.beat_schedule = {
    'check_payment_status-every-20-seconds': {
        'task': 'tasks.check_payment_status',
        'schedule': 20.0,
        'args': (100, )
    },
}


HOSTNAME = socket.gethostname()
