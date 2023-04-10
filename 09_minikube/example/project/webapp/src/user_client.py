from google.protobuf.json_format import MessageToJson
from typing import List

from client_base import ClientBase
import user_pb2
import user_pb2_grpc


class UserClient(ClientBase): 
    SERVER_DNS = "user"

    @classmethod
    async def async_get_credit_card(
        cls,
        user_ids: List[int],
    ) -> List[str]:
        async with cls.get_channel() as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.GetCreditCardRequest(
                user_ids=user_ids,
            )
            response = await stub.GetCreditCard(request)
            return [MessageToJson(card) for card in response.credit_cards]
        
