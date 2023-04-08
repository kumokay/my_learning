import asyncio
import grpc
import logging
from datetime import datetime, timedelta

from auction_pb2 import (
    Auction,
    GetAuctionsRequest,
    GetAuctionsReply,
    CreateAuctionRequest,
    CreateAuctionReply,
    PaymentCompleteRequest,
    PaymentCompleteReply,
)
from auction_pb2_grpc import (
    AuctionService,
    add_AuctionServiceServicer_to_server,
)
from query import QueryExecutor


class AuctionServer(AuctionService):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    async def CreateAuction(
        self,
        request: CreateAuctionRequest,
        context: grpc.aio.ServicerContext,
    ) -> CreateAuctionReply:
        logging.info("[CreateAuction] Serving request %s", request)
        start_at = datetime.now()
        end_at = start_at + timedelta(days=10)
        status = 'ongoing'
        count = QueryExecutor.create_auction(
            request.auction_name, 
            request.seller_id, 
            request.price,
            start_at.strftime(self.DATETIME_FORMAT),
            end_at.strftime(self.DATETIME_FORMAT),
            status,
        )
        return CreateAuctionReply(
            message=f"[CreateAuction] user-{request.seller_id} listed {count} "
                    f"auction-{request.auction_name} at ${request.price}"
        )

    async def GetAuctions(
        self,
        request: GetAuctionsRequest,
        context: grpc.aio.ServicerContext,
    ) -> GetAuctionsReply:
        logging.info("[GetAuctions] Serving request %s", request)
        result = QueryExecutor.get_auctions(
            request.next_auction_id, 
            request.limit
        )
        auctions = [
            Auction(
                auction_id=item.auction_id, 
                auction_name=item.auction_name,
                start_price=item.start_price,
                seller_name=item.seller_name,
                start_at=item.start_at,
                end_at=item.end_at,
                status=item.status,
            ) for item in result
        ]
        next_auction_id = (
            -1 if len(auctions) < request.limit 
            else auctions[-1].auction_id + 1
        )
        return GetAuctionsReply(auctions=auctions, next_auction_id=next_auction_id)
        
    async def PaymentComplete(
        self,
        request: PaymentCompleteRequest,
        context: grpc.aio.ServicerContext,
    ) -> PaymentCompleteReply:
        logging.info("[PaymentComplete] Serving request %s", request)
        status = 'completed'
        count = QueryExecutor.update_payments(
            request.payment_ids,
            status,
        )
        return PaymentCompleteReply(
            message=f"[PaymentComplete] {count} payment-{request.payment_ids} is {status}"
        )

SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_AuctionServiceServicer_to_server(AuctionServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
