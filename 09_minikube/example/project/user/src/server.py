import asyncio
import grpc
import logging
from datetime import datetime, timedelta

from user_pb2 import (
    CreditCard,
    GetCreditCardRequest,
    GetCreditCardReply,
)
from user_pb2_grpc import (
    UserService,
    add_UserServiceServicer_to_server,
)
from query import QueryExecutor


class UserServer(UserService):

    async def GetCreditCard(
        self,
        request: GetCreditCardRequest,
        context: grpc.aio.ServicerContext,
    ) -> GetCreditCardReply:
        logging.info("[GetCreditCard] Serving request %s", request)
        result = QueryExecutor.get_credit_card(
            request.user_ids, 
        )
        credit_cards = [
            CreditCard(
                card_holder_name=item.card_holder_name,
                card_number=item.card_number,
            ) for item in result
        ]
        return GetCreditCardReply(credit_cards=credit_cards)


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_UserServiceServicer_to_server(UserServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
