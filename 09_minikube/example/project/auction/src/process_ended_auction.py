import asyncio
import grpc
import logging
from typing import List
from datetime import datetime

from query import QueryExecutor
import bidding_pb2
import bidding_pb2_grpc
import user_pb2
import user_pb2_grpc
import payment_pb2
import payment_pb2_grpc


class ProcessEndedAuction:
    SERVER_PORT = 50051
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def _get_channel(cls, server_dns) -> grpc.aio.Channel:
        target = f"{server_dns}:{cls.SERVER_PORT}"
        return grpc.aio.insecure_channel(target)

    @classmethod
    async def _async_get_highest_bid_from_leader(
            cls,
            auction_ids_filter: List[int],
        ) -> List[bidding_pb2.Bid]:
            async with cls._get_channel("bidding") as channel:
                stub = bidding_pb2_grpc.BiddingServiceStub(channel)
                request = bidding_pb2.HighestBidRequest(
                    auction_ids_filter=auction_ids_filter,
                    read_from_leader=True,
                )
                response = await stub.GetHighestBid(request)
                return response.bids

    @classmethod
    async def _async_get_credit_card(
        cls,
        user_ids: int,
    ) -> List[user_pb2.CreditCard]:
        async with cls._get_channel("user") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.GetCreditCardRequest(
                user_ids=user_ids,
            )
            response = await stub.GetCreditCard(request)
            return response.credit_cards
        
    @classmethod
    async def _async_process_payment(
        cls,
        payment_id: int,
        card_holder_name: str,
        card_number: str,
        price: float,
    ) -> str:
        async with cls._get_channel("payment") as channel:
            stub = payment_pb2_grpc.PaymentServiceStub(channel)
            request = payment_pb2.ProcessPaymentRequest(
                payment_id=payment_id,
                card_holder_name=card_holder_name,
                card_number=card_number,
                price=price,
            )
            response = await stub.ProcessPayment(request)
            return response.message

    @classmethod
    async def run(cls) -> None:
        logging.info("[ProcessEndedAuction] get ended auctions")
        next_auction_id = 0
        status_filter = "ended"
        limit = 100
        ended_auctions = QueryExecutor.get_auctions(
            next_auction_id, 
            status_filter,
            limit
        )
        ended_auction_ids = [auction.id for auction in ended_auctions]
        
        logging.info(f"[ProcessEndedAuction] get winners of auctions-{ended_auction_ids}")
        highest_bids = await cls._async_get_highest_bid_from_leader(ended_auction_ids)
        user_ids = [bid.bidder_id for bid in highest_bids]

        logging.info(f"[ProcessEndedAuction] get credit card info of users-{user_ids}")
        credit_cards = await cls._async_get_credit_card(user_ids)

        logging.info("[ProcessEndedAuction] create payment entries")
        payment_ids: List[int] = []
        for highest_bid in highest_bids:
            create_at = datetime.now()
            status = 'pending'
            lastrowid = QueryExecutor.create_payment(
                highest_bid.bid_id,
                highest_bid.auction_id,
                highest_bid.bidder_id,
                highest_bid.bid_price,
                create_at.strftime(cls.DATETIME_FORMAT),
                status,
            )
            payment_ids.append(lastrowid)
        
        logging.info(f"[ProcessEndedAuction] initiate payments-{payment_ids}")
        payments: List[payment_pb2.Payment] = []
        for idx in range(len(payment_ids)):
            payment = payment_pb2.Payment(
                payment_id=payment_ids[idx],
                card_number=credit_cards[idx].card_number,
                card_holder_name=credit_cards[idx].card_holder_name,
                price=highest_bids[idx].bid_price,
            )
            payments.append(payment)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("[process_ended_auction] started ===")
    asyncio.run(ProcessEndedAuction.run())
    logging.info("[process_ended_auction] ended ===")



