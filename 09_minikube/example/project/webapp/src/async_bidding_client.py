import asyncio
import logging
import grpc
from typing import List
from google.protobuf.json_format import MessageToJson

import bidding_pb2
import bidding_pb2_grpc
import bidding_pb2
import bidding_pb2_grpc


class ClientBase:
    SERVER_DNS = "localhost"
    SERVER_PORT = 50051

    @classmethod
    def target(cls):
        return f"{cls.SERVER_DNS}:{cls.SERVER_PORT}"


class WriterClient(ClientBase):
    SERVER_DNS = "writer"

    @classmethod
    async def async_list_product(
            cls,
            product_name: str,
            seller_id: int,
            price: float) -> str:
        async with grpc.aio.insecure_channel(cls.target()) as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.ListRequest(
                    product_name=product_name,
                    seller_id=seller_id,
                    price=price)
            response = await stub.ListProduct(request)
            return response.message

    @classmethod
    async def async_place_bid(
            cls,
            product_id: int,
            bidder_id: int,
            price: float) -> str:
        async with grpc.aio.insecure_channel(cls.target()) as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.BidRequest(
                    product_id=product_id,
                    bidder_id=bidder_id,
                    price=price)
            response = await stub.PlaceBid(request)
            return response.message


class ReaderClient(ClientBase):
    SERVER_DNS = "reader"

    @classmethod
    async def async_get_catalogue(
            cls,
            next_product_id: int,
            limit: int) -> List[str]:
        async with grpc.aio.insecure_channel(cls.target()) as channel:
            stub = bidding_pb2_grpc.BiddingServiceStub(channel)
            request = bidding_pb2.CatalogueRequest(
                    next_product_id=next_product_id,
                    limit=limit)
            response = await stub.GetCatalogue(request)
            return [MessageToJson(product) for product in response.products]
