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

from bidding_read_pb2 import CatalogueRequest, CatalogueReply
from bidding_read_pb2_grpc import BiddingReadService
from bidding_read_pb2_grpc import add_BiddingReadServiceServicer_to_server
# from tasks import list_product, place_bid


class BiddingReader(BiddingReadService):

    async def GetCatalogue(
            self, 
            request: CatalogueRequest,
            context: grpc.aio.ServicerContext) -> CatalogueReply:
        logging.info("[GetCatalogue] Serving request %s", request)
        # task = list_product.s(request.product_name, request.seller_id, request.price).apply_async()
        # result = task.get()
        products = [
                CatalogueReply.Product(id=n, name=f"product{n}", price=n*2, seller_id=n+1)
                for n in range(5)
	]
        return CatalogueReply(products=products, next_product_id=0)


SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_BiddingReadServiceServicer_to_server(BiddingReader(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

