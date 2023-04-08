import socket
import logging
from typing import List
from celery import Celery
import grpc
import asyncio

from query import QueryExecutor, TransactionObj
from third_party_payment_process import ThirdPartyPaymentProcess

import auction_pb2
import auction_pb2_grpc


app = Celery(broker='redis://payment-redis-leader:6379/0',
             backend='redis://payment-redis-leader:6379/1')


# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


HOSTNAME = socket.gethostname()


@app.task
def process_payment(
    payment_id: int,
    card_holder_name: str,
    card_number: str,
    price: float,
    initiated_at: str,
) -> str:
    result = QueryExecutor.select_transaction_by_payment_id(
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


async def async_payment_complete(
    payment_ids: List[int],
) -> List[str]:
    server_dns = "auction"
    server_port = 50051
    target = f"{server_dns}:{server_port}"
    async with grpc.aio.insecure_channel(target) as channel:
        stub = auction_pb2_grpc.AuctionServiceStub(channel)
        request = auction_pb2.PaymentCompleteRequest(
            payment_ids=payment_ids,
        )
        response = await stub.PaymentComplete(request)
        return response.message


@app.task
def check_payment_status(limit: int) -> str:
    logging.info(f"[check_payment_status] periodic task started")
    # get all transactions in process
    status = 'processing'
    result = QueryExecutor.select_transaction_by_status(
        status,
        limit,
    )
    logging.info(f"[check_payment_status] checking {len(result)} transactions")
    completed_transactions: List[TransactionObj] = []
    for tx in result: 
        is_completed = ThirdPartyPaymentProcess.IsPaymentCompleted(
            tx.third_party_transaction_id,
        )
        if is_completed:
            completed_transactions.append(tx)

    # update completed transactions
    status = 'completed'
    for tx in completed_transactions:
        count = QueryExecutor.update_transaction(
            tx.id,
            tx.payment_id, 
            tx.third_party_transaction_id, 
            status,
        )
        logging.info(
            f"[check_payment_status] {count} payment-{tx.payment_id} "
            f"transaction-{tx.third_party_transaction_id} is completed")
        
    # update completed payments
    payment_ids = [tx.payment_id for tx in completed_transactions]
    response = asyncio.run(async_payment_complete(payment_ids))
    logging.info(f"[check_payment_status] {response}")
    return "[check_payment_status] task completed"