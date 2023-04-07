from random import randrange
import socket
import time

from celery import Celery
from query import QueryExecutor


app = Celery(broker='redis://payment-redis-leader:6379/0',
             backend='redis://payment-redis-leader:6379/1')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


HOSTNAME = socket.gethostname()
EXECTIME = 3


class ThirdPartyPaymentProcess:
    THIRD_PARTY_TRX_ID = 100  # static var

    @classmethod
    def ProcessPayment(cls) -> str:
        # add delay
        time.sleep(EXECTIME)
        cls.THIRD_PARTY_TRX_ID = cls.THIRD_PARTY_TRX_ID + 1
        return f"transaction-{cls.THIRD_PARTY_TRX_ID}"
    
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
    result = QueryExecutor.select_transaction(
        payment_id,
    )
    if len(result) != 0:
        return (
            f"[{HOSTNAME}] cannot process payment-{payment_id} ${price} "
            f"for {card_holder_name} with card {card_number}, "
            f"existing transactions={result}"
        )
    
    third_party_transaction_id = ""
    status = "initiating"
    transaction_id = QueryExecutor.insert_transaction(
        payment_id, 
        card_holder_name, 
        card_number, 
        price, 
        third_party_transaction_id, 
        initiated_at, 
        status,
    )
    
    third_party_transaction_id = ThirdPartyPaymentProcess.ProcessPayment()
    status = "processing"
    count = QueryExecutor.update_transaction(
        transaction_id,
        payment_id, 
        third_party_transaction_id, 
        status,
    )
    
    return (
        f"[{HOSTNAME}] process {count} payment-{payment_id} ${price} "
        f"for {card_holder_name} with card {card_number}, "
        f"transaction_id={third_party_transaction_id}"
    )

