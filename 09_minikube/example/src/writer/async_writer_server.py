# Copyright 2021 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import celery
import grpc
import logging
import time

from bidding_write_pb2 import ListRequest, ListReply, BidRequest, BidReply
from bidding_write_pb2_grpc import BiddingWriteService
from bidding_write_pb2_grpc import add_BiddingWriteServiceServicer_to_server
from tasks import list_product, place_bid


class BiddingWriter(BiddingWriteService):

    async def ListProduct(
            self, 
            request: ListRequest,
            context: grpc.aio.ServicerContext) -> ListReply:
        logging.info("[ListProduct] Serving request %s", request)
        task = list_product.s(request.product_name, request.seller_id, request.price).apply_async()
        result = task.get()
        return ListReply(message=f"[ListProduct] Reply from celery-worker: {result}")

    async def PlaceBid(self, request: BidRequest,
                       context: grpc.aio.ServicerContext) -> BidReply:
        logging.info("[PlaceBid] Serving request %s", request)
        bid_at = time.strftime('%Y-%m-%d %H:%M:%S')
        task = place_bid.s(request.product_id, request.bidder_id, request.price, bid_at).apply_async()
        result = task.get()
        return BidReply(message=f"[placeBid] Reply from celery-worker: {result}")


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_BiddingWriteServiceServicer_to_server(BiddingWriter(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

