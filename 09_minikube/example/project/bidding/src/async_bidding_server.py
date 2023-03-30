import asyncio
import grpc
import logging
import time

from bidding_pb2 import (
    BidRequest,
    BidReply,
    Product,
    CatalogueRequest,
    CatalogueReply,
    ListRequest,
    ListReply,
    WinnerRequest,
    WinnerReply,
    Bid,
    BidHistoryRequest,
    BidHistoryReply,
)
from bidding_pb2_grpc import (
    BiddingService,
    add_BiddingServiceServicer_to_server,
)
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
            Product(
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

    async def GetWinner(
        self,
        request: WinnerRequest,
        context: grpc.aio.ServicerContext,
    ) -> WinnerReply:
        logging.info("[GetWinner] Serving request %s", request)
        result = QueryExecutor.get_winner(request.product_id_filter)
        bids = [
            Bid(
                bid_id=item.bid_id,
                product_id=item.product_id, 
                bidder_id=item.bidder_id,
                bid_price=item.bid_price,
                bid_at=item.bid_at,
            ) for item in result
        ]
        return WinnerReply(bids=bids)
    
    async def GetBidHistory(
        self,
        request: BidHistoryRequest,
        context: grpc.aio.ServicerContext,
    ) -> BidHistoryReply:
        logging.info("[GetBidHistory] Serving request %s", request)
        result = QueryExecutor.get_bid_history(
            request.product_id_filter,
            request.next_bid_id,
            request.limit,
        )
        bids = [
            Bid(
                bid_id=item.bid_id,
                product_id=item.product_id, 
                bidder_id=item.bidder_id,
                bid_price=item.bid_price,
                bid_at=item.bid_at,
            ) for item in result
        ]
        next_bid_id = (
            -1 if len(bids) < request.limit 
            else bids[-1].bid_id + 1
        )
        return BidHistoryReply(bids=bids, next_bid_id=next_bid_id)
        

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
