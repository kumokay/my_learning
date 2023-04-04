from google.protobuf.json_format import MessageToJson

from client_base import ClientBase

import bidding_pb2
import bidding_pb2_grpc


class BidClient(ClientBase):
    SERVER_DNS = "bid"

    @classmethod
    async def async_place_bid(
        cls,
        auction_id: int,
        bidder_id: int,
        price: float
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.BidRequest(
                auction_id=auction_id,
                bidder_id=bidder_id,
                price=price)
            response = await stub.PlaceBid(request)
            return response.message
        
    @classmethod
    async def async_get_winner(
        cls,
        auction_id_filter: int,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.WinnerRequest(
                auction_id_filter=auction_id_filter,
            )
            response = await stub.GetWinner(request)
            return [MessageToJson(bid) for bid in response.bids]
        
    @classmethod
    async def async_get_bid_history(
        cls,
        auction_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.BidHistoryRequest(
                auction_id_filter=auction_id_filter,
                next_bid_id=next_bid_id,
                limit=limit,
            )
            response = await stub.GetBidHistory(request)
            return [MessageToJson(bid) for bid in response.bids]

