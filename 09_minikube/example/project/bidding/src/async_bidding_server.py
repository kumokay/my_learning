import asyncio
import celery
import grpc
import logging
import time

from bidding_pb2 import (
    BidRequest,
    BidReply,
    CatalogueRequest,
    CatalogueReply,
    ListRequest,
    ListReply,
)
from bidding_pb2_grpc import BiddingService
from bidding_pb2_grpc import add_BiddingServiceServicer_to_server
from tasks import list_product, place_bid


class BiddingServer(BiddingWriteService):

    async def ListProduct(
            self,
            request: ListRequest,
            context: grpc.aio.ServicerContext) -> ListReply:
        logging.info("[ListProduct] Serving request %s", request)
        task = list_product.s(
            request.product_name, request.seller_id, request.price
        ).apply_async()
        result = task.get()
        return ListReply(
            message=f"[ListProduct] Reply from celery-worker: {result}"
        )

    async def PlaceBid(self, request: BidRequest,
                       context: grpc.aio.ServicerContext) -> BidReply:
        logging.info("[PlaceBid] Serving request %s", request)
        bid_at = time.strftime('%Y-%m-%d %H:%M:%S')
        task = place_bid.s(
            request.product_id, request.bidder_id, request.price, bid_at
        ).apply_async()
        result = task.get()
        return BidReply(
            message=f"[placeBid] Reply from celery-worker: {result}"
        )

    async def GetCatalogue(
            self,
            request: CatalogueRequest,
            context: grpc.aio.ServicerContext) -> CatalogueReply:
        logging.info("[GetCatalogue] Serving request %s", request)
        products = [
            CatalogueReply.Product(
                id=n, name=f"product{n}", price=n*2, seller_id=n+1
            ) for n in range(5)
        ]
        return CatalogueReply(products=products, next_product_id=0)


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_BiddingWriteServiceServicer_to_server(BiddingServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
