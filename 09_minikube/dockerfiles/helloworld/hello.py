from flask import Flask, jsonify, request
from redis import Redis
import traceback


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


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

