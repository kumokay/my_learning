import asyncio
import grpc
import logging

from product_pb2 import (
    Product,
    CatalogueRequest,
    CatalogueReply,
    ListRequest,
    ListReply,
)
from product_pb2_grpc import (
    ProductService,
    add_ProductServiceServicer_to_server,
)
from query import QueryExecutor


class ProductServer(ProductService):

    async def ListProduct(
        self,
        request: ListRequest,
        context: grpc.aio.ServicerContext,
    ) -> ListReply:
        logging.info("[ListProduct] Serving request %s", request)
        count = QueryExecutor.list_product(
            request.product_name, 
            request.seller_id, 
            request.price,
        )
        return ListReply(
            message=f"[ListProduct] user-{request.seller_id} listed {count} "
                    f"product-{request.product_name} at ${request.price}"
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
        

SERVER_PORT = 50051


async def serve() -> None:
    server = grpc.aio.server()
    add_ProductServiceServicer_to_server(ProductServer(), server)
    listen_addr = f"[::]:{SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
