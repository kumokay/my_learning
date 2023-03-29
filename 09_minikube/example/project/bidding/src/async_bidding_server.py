import asyncio
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
from query import QueryExecutor


class BiddingServer(BiddingService):

    async def ListProduct(
        self,
        request: ListRequest,
        context: grpc.aio.ServicerContext,
    ) -> ListReply:
        logging.info("[ListProduct] Serving request %s", request)
        task = list_product.s(
            request.product_name, request.seller_id, request.price
        ).apply_async()
        result = task.get()
        return ListReply(
            message=f"[ListProduct] Reply from celery-worker: {result}"
        )

    async def PlaceBid(
        self, 
        request: BidRequest,
        context: grpc.aio.ServicerContext,
    ) -> BidReply:
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
        context: grpc.aio.ServicerContext,
    ) -> CatalogueReply:
        logging.info("[GetCatalogue] Serving request %s", request)
        result = QueryExecutor.get_catalogue(
            request.next_product_id, 
            request.limit
        )
        products = [
            CatalogueReply.Product(
                product_id=item.product_id, 
                product_name=item.product_name,
                product_price=item.product_price,
                seller_name=item.seller_name,
            ) for item in result
        ]
        next_product_id = (
            -1 if len(products) < request.limit 
            else products[-1].product_id + 1
        )
        return CatalogueReply(products=products, next_product_id=next_product_id)


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_BiddingServiceServicer_to_server(BiddingServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
