from random import randrange
import socket
import time

from celery import Celery
from query import QueryExecutor


app = Celery(broker='redis://payment-redis-leader:6379/0',
             backend='redis://payment-leader:6379/1')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


HOSTNAME = socket.gethostname()
EXECTIME = 3

THIRD_PARTY_TRX_ID = 100

class ThirdPartyPaymentProcess:
    @staticmethod
    def ProcessPayment() -> str:
        # add delay
        time.sleep(EXECTIME)
        THIRD_PARTY_TRX_ID = THIRD_PARTY_TRX_ID + 1
        return f"transaction-{THIRD_PARTY_TRX_ID}"
    
    @staticmethod
    def isPaymentCompleted() -> bool:
        return randrange(5) == 0  # 1/5 chance




@app.task
def process_payment(
    payment_id: int,
    card_holder_name: str,
    card_number: str,
    price: float,
    initiated_at: str,
) -> str:
    third_party_transaction_id = ""
    status = "initiating"
    count = QueryExecutor.insert_transaction(
        payment_id, 
        card_holder_name, 
        card_number, 
        price, 
        third_party_transaction_id, 
        initiated_at, 
        status,
    )
    assert(count == 1)
    
    third_party_transaction_id = ThirdPartyPaymentProcess.ProcessPayment()
    status = "processing"
    count = QueryExecutor.update_transaction(
        payment_id, 
        third_party_transaction_id, 
        status,
    )
    assert(count == 1)
    
    return (
        f"[{HOSTNAME}] process payment-{payment_id} ${price} "
        f"for {card_holder_name} with card {card_number}, "
        f"transaction_id={third_party_transaction_id}"
    )

