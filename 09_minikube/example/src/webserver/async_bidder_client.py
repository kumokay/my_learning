import asyncio
import logging
import grpc

import bidding_write_pb2
import bidding_write_pb2_grpc


SERVER_DNS = "writer"
SERVER_PORT = 50051


class WriterClient:
    @classmethod
    async def async_list_product(
            cls,
            product_name: str,
            seller_id: int,
            price: float) -> str:
        async with grpc.aio.insecure_channel(f"{SERVER_DNS}:{SERVER_PORT}") as channel:
            stub = bidding_write_pb2_grpc.BiddingWriteServiceStub(channel)
            request = bidding_write_pb2.ListRequest(
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
        async with grpc.aio.insecure_channel(f"{SERVER_DNS}:{SERVER_PORT}") as channel:
            stub = bidding_write_pb2_grpc.BiddingWriteServiceStub(channel)
            request = bidding_write_pb2.BidRequest(
                    product_id=product_id,
                    bidder_id=bidder_id,
                    price=price)
            response = await stub.PlaceBid(request)
            return response.message

