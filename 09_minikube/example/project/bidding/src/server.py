import asyncio
import grpc
import logging
import time

from bidding_pb2 import (
    BidRequest,
    BidReply,
    HighestBidRequest,
    HighestBidReply,
    Bid,
    BidHistoryRequest,
    BidHistoryReply,
)
from bidding_pb2_grpc import (
    BiddingService,
    add_BiddingServiceServicer_to_server,
)
from tasks import place_bid
from query import QueryExecutor


class BiddingServer(BiddingService):

    async def PlaceBid(
        self, 
        request: BidRequest,
        context: grpc.aio.ServicerContext,
    ) -> BidReply:
        logging.info("[PlaceBid] Serving request %s", request)
        bid_at = time.strftime('%Y-%m-%d %H:%M:%S')
        task = place_bid.s(
            request.auction_id, request.bidder_id, request.price, bid_at
        ).apply_async()
        result = task.get()
        return BidReply(
            message=f"[placeBid] Reply from celery-worker: {result}"
        )

    async def GetHighestBid(
        self,
        request: HighestBidRequest,
        context: grpc.aio.ServicerContext,
    ) -> HighestBidReply:
        logging.info("[GetHighestBid] Serving request %s", request)
        result = QueryExecutor.get_highest_bid(
            request.auction_id_filter, 
            request.read_from_leader,
        )
        bids = [
            Bid(
                bid_id=item.bid_id,
                auction_id=item.auction_id, 
                bidder_id=item.bidder_id,
                bid_price=item.bid_price,
                bid_at=item.bid_at,
            ) for item in result
        ]
        return HighestBidReply(bids=bids)
    
    async def GetBidHistory(
        self,
        request: BidHistoryRequest,
        context: grpc.aio.ServicerContext,
    ) -> BidHistoryReply:
        logging.info("[GetBidHistory] Serving request %s", request)
        result = QueryExecutor.get_bid_history(
            request.auction_id_filter,
            request.next_bid_id,
            request.limit,
        )
        bids = [
            Bid(
                bid_id=item.bid_id,
                auction_id=item.auction_id, 
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
