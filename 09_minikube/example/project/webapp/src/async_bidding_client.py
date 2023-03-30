import grpc
from typing import List
from google.protobuf.json_format import MessageToJson

import bidding_pb2
import bidding_pb2_grpc


class ClientBase:
    SERVER_DNS = "localhost"
    SERVER_PORT = 50051

    @classmethod
    def get_channel(cls) -> grpc.aio.Channel:
        target = f"{cls.SERVER_DNS}:{cls.SERVER_PORT}"
        return grpc.aio.insecure_channel(target)


class BidClient(ClientBase):
    SERVER_DNS = "bid"

    @classmethod
    async def async_place_bid(
        cls,
        product_id: int,
        bidder_id: int,
        price: float
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.BidRequest(
                product_id=product_id,
                bidder_id=bidder_id,
                price=price)
            response = await stub.PlaceBid(request)
            return response.message
        
    @classmethod
    async def async_get_winner(
        cls,
        product_id_filter: int,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.WinnerRequest(
                product_id_filter=product_id_filter,
            )
            response = await stub.GetWinner(request)
            return [MessageToJson(bid) for bid in response.bids]
        
    @classmethod
    async def async_get_bid_history(
        cls,
        product_id_filter: int,
        next_bid_id: int,
        limit: int
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.BidHistoryRequest(
                product_id_filter=product_id_filter,
                next_bid_id=next_bid_id,
                limit=limit,
            )
            response = await stub.GetBidHistory(request)
            return [MessageToJson(bid) for bid in response.bids]


class ProductClient(ClientBase): 
    SERVER_DNS = "product"

    @classmethod
    async def async_list_product(
        cls,
        product_name: str,
        seller_id: int,
        price: float,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.ListRequest(
                product_name=product_name,
                seller_id=seller_id,
                price=price,
            )
            response = await stub.ListProduct(request)
            return response.message

    @classmethod
    async def async_get_catalogue(
        cls,
        next_product_id: int,
        limit: int
    ) -> List[str]:
        async with cls.get_channel() as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.CatalogueRequest(
                next_product_id=next_product_id,
                limit=limit,
            )
            response = await stub.GetCatalogue(request)
            return [MessageToJson(product) for product in response.products]
