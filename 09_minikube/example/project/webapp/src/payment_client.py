from google.protobuf.json_format import MessageToJson

from client_base import ClientBase
import payment_pb2
import payment_pb2_grpc


class PaymentClient(ClientBase): 
    SERVER_DNS = "payment"

    @classmethod
    async def async_process_payment(
        cls,
        payment_id: int,
        card_holder_name: str,
        card_number: str,
        price: float,
    ) -> str:
        async with cls.get_channel() as channel:
            stub = payment_pb2_grpc.PaymentServiceStub(channel)
            payment = payment_pb2.Payment(
                payment_id=payment_id,
                card_holder_name=card_holder_name,
                card_number=card_number,
                price=price,
            )
            request = payment_pb2.ProcessPaymentRequest(
                payments=[payment],
            )
            response = await stub.ProcessPayment(request)
            return response.message
        
