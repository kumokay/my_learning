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


class PaymentServer(PaymentService):

    async def ProcessPayment(
        self, 
        request: ProcessPaymentRequest,
        context: grpc.aio.ServicerContext,
    ) -> ProcessPaymentReply:
        logging.info("[ProcessPayment] Serving request %s", request)
        for payment in request.payments:
            initiated_at = time.strftime('%Y-%m-%d %H:%M:%S')
            task = process_payment.s(
                payment.payment_id,
                payment.card_holder_name,
                payment.card_number,
                payment.price,
                initiated_at,
            ).apply_async()
            task.forget()
        return ProcessPaymentReply(
            message=f"[ProcessPayment] Sent task-process_payment to celery-worker"
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
