from typing import List
from google.protobuf.json_format import MessageToJson

from client_base import ClientBase
import auction_pb2
import auction_pb2_grpc


class AuctionClient(ClientBase): 
    SERVER_DNS = "auction"

    @classmethod
    async def async_create_auction(
        cls,
        auction_name: str,
        seller_id: int,
        price: float,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = auction_pb2_grpc.AuctionServiceStub(channel)
            request = auction_pb2.CreateAuctionRequest(
                auction_name=auction_name,
                seller_id=seller_id,
                price=price,
            )
            response = await stub.CreateAuction(request)
            return response.message

    @classmethod
    async def async_get_auctions(
        cls,
        next_auction_id: int,
        status_filter: str,
        limit: int
    ) -> List[str]:
        async with cls.get_channel() as channel:
            stub = auction_pb2_grpc.AuctionServiceStub(channel)
            request = auction_pb2.GetAuctionsRequest(
                next_auction_id=next_auction_id,
                status_filter=status_filter,
                limit=limit,
            )
            response = await stub.GetAuctions(request)
            return [MessageToJson(auction) for auction in response.auctions]
        
    @classmethod
    async def async_payment_complete(
        cls,
        payment_ids: List[int],
    ) -> List[str]:
        async with cls.get_channel() as channel:
            stub = auction_pb2_grpc.AuctionServiceStub(channel)
            request = auction_pb2.PaymentCompleteRequest(
                payment_ids=payment_ids,
            )
            response = await stub.PaymentComplete(request)
            return response.message