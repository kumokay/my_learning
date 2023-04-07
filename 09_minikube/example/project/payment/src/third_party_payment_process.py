import logging
from random import randrange
import time

class ThirdPartyPaymentProcess:
    EXECTIME = 3
    THIRD_PARTY_TRX_ID = 100  # static var

    @classmethod
    def ProcessPayment(cls) -> str:
        # add delay
        time.sleep(cls.EXECTIME)
        cls.THIRD_PARTY_TRX_ID = cls.THIRD_PARTY_TRX_ID + 1
        return f"transaction-{cls.THIRD_PARTY_TRX_ID}"
    
    @classmethod
    def IsPaymentCompleted(cls, transaction_id: int) -> bool:
        is_completed = randrange(5) == 0
        logging.info(
            f"[IsPaymentCompleted] transaction {transaction_id} "
            f"is completed? {is_completed}"
        )
        # add delay
        time.sleep(cls.EXECTIME)
        return is_completed # 1/5 chance
    
