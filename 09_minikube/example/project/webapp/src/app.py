"""
Tutorials:
- Flask: https://www.geeksforgeeks.org/flask-app-routing/
- Redis: https://developer.redis.com/develop/python/
"""
from flask import Flask, jsonify, request
from redis import Redis

from bidding_client import BidClient
from product_client import ProductClient


app = Flask(__name__)


@app.get("/")
def hello():
    return "Hello World!"


@app.get("/list_product/<string:product_name>/<int:seller_id>/<float:price>/")
async def list_product_for_testing(product_name: str, seller_id: int, price: float):
    result = await ProductClient.async_list_product(product_name, seller_id, price)
    return jsonify([result])


@app.post("/list_product/")
async def list_product():
    product_name = request.json['product_name']
    seller_id = request.json['seller_id']
    price = request.json['price']
    result = await ProductClient.async_list_product(product_name, seller_id, price)
    return jsonify([result])


@app.get("/get_catalogue/<int:next_product_id>/<int:limit>/")
async def get_catalogue(next_product_id: int, limit: int):
    result = await ProductClient.async_get_catalogue(next_product_id, limit)
    return jsonify([result])


@app.get("/place_bid/<int:product_id>/<int:bidder_id>/<float:price>/")
async def place_bid_for_testing(product_id: int, bidder_id: int, price: float):
    result = await BidClient.async_place_bid(product_id, bidder_id, price)
    return jsonify([result])


@app.post("/place_bid/")
async def place_bid():
    product_id = request.json['product_id']
    bidder_id = request.json['bidder_id']
    price = request.json['price']
    result = await BidClient.async_place_bid(product_id, bidder_id, price)
    return jsonify([result])


@app.get("/get_bid_history/<int:product_id_filter>/<int:next_bid_id>/<int:limit>/")
async def get_bid_history(product_id_filter: int, next_bid_id: int, limit: int):
    result = await BidClient.async_get_bid_history(product_id_filter, next_bid_id, limit)
    return jsonify([result])


@app.get("/get_winner/<int:product_id_filter>/",)
async def get_winner(product_id_filter: int):
    result = await BidClient.async_get_winner(product_id_filter)
    return jsonify([result])


g_data = [{"default": 100}]


@app.route("/get_data")
def get_data():
    return jsonify(g_data)


@app.route("/add_data", methods=["POST"])
def add_data():
    g_data.append(request.get_json())
    return jsonify(g_data)


REDIS_LEADER_DNS = "redis-leader"
REDIS_FOLLOWER_DNS = "redis-follower"
REDIS_PORT = 6379
REDIS_DB = 0


@app.route("/get_from_redis")
def get_from_redis():
    r = Redis(host=REDIS_FOLLOWER_DNS, port=REDIS_PORT, db=REDIS_DB)
    byte_keys = r.keys()
    byte_vals = r.mget(byte_keys)
    keys = [x.decode('utf-8') for x in byte_keys]
    vals = [x.decode('utf-8') for x in byte_vals]
    return jsonify([dict(zip(keys, vals))])


@app.route("/add_to_redis", methods=["POST"])
def add_to_redis():
    r = Redis(host=REDIS_LEADER_DNS, port=REDIS_PORT, db=REDIS_DB)
    r.mset(request.get_json())
    # read from leader
    byte_keys = r.keys()
    byte_vals = r.mget(byte_keys)
    keys = [x.decode('utf-8') for x in byte_keys]
    vals = [x.decode('utf-8') for x in byte_vals]
    return jsonify([dict(zip(keys, vals))])
