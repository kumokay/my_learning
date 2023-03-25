import socket
import time

from celery import Celery


app = Celery('tasks',
             broker='redis://redis-leader:6379/0',
             backend='redis://redis-leader:6379/0')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


@app.task
def greet(name: str, num: int) -> str:
    time.sleep(3)
    return f"Hello #{num} from {socket.gethostname()}, {name}!"

