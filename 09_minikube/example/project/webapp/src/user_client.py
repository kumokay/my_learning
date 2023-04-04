from google.protobuf.json_format import MessageToJson

from client_base import ClientBase
import user_pb2
import user_pb2_grpc


class UserClient(ClientBase): 
    SERVER_DNS = "user"

    @classmethod
    async def async_get_credit_card(
        cls,
        user_id: int,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.GetCreditCardRequest(
                user_id=user_id,
            )
            response = await stub.GetCreditCard(request)
            return MessageToJson(response.credit_card)
        
