import asyncio
import grpc
import logging
import time

from payment_pb2 import (
    ProcessPaymentRequest,
    ProcessPaymentReply,
)
from payment_pb2_grpc import (
    PaymentService,
    add_PaymentServiceServicer_to_server,
)
from tasks import process_payment
from query import QueryExecutor


class PaymentServer(PaymentService):

    async def ProcessPayment(
        self, 
        request: ProcessPaymentRequest,
        context: grpc.aio.ServicerContext,
    ) -> ProcessPaymentReply:
        logging.info("[ProcessPayment] Serving request %s", request)
        initiated_at = time.strftime('%Y-%m-%d %H:%M:%S')
        task = process_payment.s(
            request.payment_id,
            request.card_holder_name,
            request.card_number,
            request.price,
            initiated_at,
        ).apply_async()
        result = task.get()
        return ProcessPaymentReply(
            message=f"[ProcessPayment] Reply from celery-worker: {result}"
        )


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_PaymentServiceServicer_to_server(PaymentServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
