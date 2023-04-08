"""
Tutorials:
- Flask: https://www.geeksforgeeks.org/flask-app-routing/
- Redis: https://developer.redis.com/develop/python/
"""
from flask import Flask, jsonify, request

from bidding_client import BidClient
from auction_client import AuctionClient
from user_client import UserClient
from payment_client import PaymentClient


app = Flask(__name__)


@app.get("/")
def hello():
    return "Hello World!"


@app.get("/create_auction/<string:auction_name>/<int:seller_id>/<float:price>/")
async def test_create_auction(auction_name: str, seller_id: int, price: float):
    result = await AuctionClient.async_create_auction(auction_name, seller_id, price)
    return jsonify([result])


@app.post("/create_auction/")
async def create_auction():
    auction_name = request.json['auction_name']
    seller_id = request.json['seller_id']
    price = request.json['price']
    result = await AuctionClient.async_create_auction(auction_name, seller_id, price)
    return jsonify([result])


@app.get("/get_auctions/<int:next_auction_id>/<int:limit>/")
async def get_auctions(next_auction_id: int, limit: int):
    result = await AuctionClient.async_get_auctions(next_auction_id, limit)
    return jsonify([result])


@app.get("/place_bid/<int:auction_id>/<int:bidder_id>/<float:price>/")
async def test_place_bid(auction_id: int, bidder_id: int, price: float):
    result = await BidClient.async_place_bid(auction_id, bidder_id, price)
    return jsonify([result])


@app.post("/place_bid/")
async def place_bid():
    auction_id = request.json['auction_id']
    bidder_id = request.json['bidder_id']
    price = request.json['price']
    result = await BidClient.async_place_bid(auction_id, bidder_id, price)
    return jsonify([result])


@app.get("/get_bid_history/<int:auction_id_filter>/<int:next_bid_id>/<int:limit>/")
async def get_bid_history(auction_id_filter: int, next_bid_id: int, limit: int):
    result = await BidClient.async_get_bid_history(auction_id_filter, next_bid_id, limit)
    return jsonify([result])


@app.get("/get_highest_bid/<int:auction_id_filter>/",)
async def get_highest_bid(auction_id_filter: int):
    result = await BidClient.async_get_highest_bid(auction_id_filter)
    return jsonify([result])


"""
TESTING
"""
@app.get("/test_get_credit_card/<int:user_id>/")
async def test_get_credit_card(user_id: int):
    result = await UserClient.async_get_credit_card(user_id)
    return jsonify([result])

@app.post("/test_payment_complete/")
async def test_payment_complete():
    payment_id = request.json['payment_id']
    result = await AuctionClient.async_payment_complete([payment_id])
    return jsonify([result])

@app.post("/test_process_payment/")
async def test_process_payment():
    payment_id = request.json['payment_id']
    card_holder_name = request.json['card_holder_name']
    card_number = request.json['card_number']
    price = request.json['price']
    result = await PaymentClient.async_process_payment(                
        payment_id,
        card_holder_name,
        card_number,
        price,
    )
    return jsonify([result])
