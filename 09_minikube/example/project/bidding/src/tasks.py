import socket
import time

from celery import Celery
from query import QueryExecutor


app = Celery(broker='redis://redis-leader:6379/0',
             backend='redis://redis-leader:6379/1')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


HOSTNAME = socket.gethostname()
EXECTIME = 3


@app.task
def place_bid(
    auction_id: int,
    bidder_id: int,
    price: float,
    bid_at: str,
) -> str:
    count = QueryExecutor.place_bid(auction_id, bidder_id, price, bid_at)
    # add delay
    time.sleep(EXECTIME)
    return (
        f"[{HOSTNAME}] user-{bidder_id} bid ${price} "
        f"for {count} auction-{auction_id}"
    )

