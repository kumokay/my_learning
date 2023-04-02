from typing import List
from google.protobuf.json_format import MessageToJson

from client_base import ClientBase
import product_pb2
import product_pb2_grpc


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
            stub = product_pb2_grpc.ProductServiceStub(channel)
            request = product_pb2.ListRequest(
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
            stub = product_pb2_grpc.ProductServiceStub(channel)
            request = product_pb2.CatalogueRequest(
                next_product_id=next_product_id,
                limit=limit,
            )
            response = await stub.GetCatalogue(request)
            return [MessageToJson(product) for product in response.products]
