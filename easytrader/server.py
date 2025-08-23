import datetime
import functools
import hashlib

from flask import Flask, jsonify, request

from . import api
from .log import logger

app = Flask(__name__)

global_store = {}


def error_handle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # pylint: disable=broad-except
        except Exception as e:
            logger.exception("server error")
            message = "{}: {}".format(e.__class__, e)
            return jsonify({"error": message}), 400

    return wrapper


@app.route("/prepare", methods=["POST"])
@error_handle
def post_prepare():
    json_data = request.get_json(force=True)

    # 添加用户登录验证
    password = json_data.get('password')
    if not password:
        return jsonify({"error": "Missing password"}), 401

    # 生成基于当前日期的hash值
    today = datetime.date.today().strftime('%Y-%m-%d')
    expected_password = hashlib.md5(today.encode('utf-8')).hexdigest()

    # 验证密码
    if password != expected_password:
        return jsonify({"error": "Invalid password"}), 401

    # 密码验证通过后，移除password字段再继续处理
    json_data.pop('password', None)

    user = api.use(json_data.pop("broker"))
    # user.connect(**json_data)
    user.connect(
        miniqmt_path=r"D:\\Apps\\国金QMT交易端模拟\\userdata_mini",  # QMT 客户端下的 miniqmt 安装路径
        stock_account="55011468",  # 资金账号
    )

    global_store["user"] = user
    return jsonify({"msg": "login success"}), 201


@app.route("/balance", methods=["GET"])
@error_handle
def get_balance():
    user = global_store["user"]
    balance = user.balance

    return jsonify(balance), 200


@app.route("/position", methods=["GET"])
@error_handle
def get_position():
    user = global_store["user"]
    position = user.position

    return jsonify(position), 200


@app.route("/auto_ipo", methods=["GET"])
@error_handle
def get_auto_ipo():
    user = global_store["user"]
    res = user.auto_ipo()

    return jsonify(res), 200


@app.route("/today_entrusts", methods=["GET"])
@error_handle
def get_today_entrusts():
    user = global_store["user"]
    today_entrusts = user.today_entrusts

    return jsonify(today_entrusts), 200


@app.route("/today_trades", methods=["GET"])
@error_handle
def get_today_trades():
    user = global_store["user"]
    today_trades = user.today_trades

    return jsonify(today_trades), 200


@app.route("/cancel_entrusts", methods=["GET"])
@error_handle
def get_cancel_entrusts():
    user = global_store["user"]
    cancel_entrusts = user.cancel_entrusts

    return jsonify(cancel_entrusts), 200


@app.route("/buy", methods=["POST"])
@error_handle
def post_buy():
    json_data = request.get_json(force=True)
    user = global_store["user"]
    res = user.buy(**json_data)

    return jsonify(res), 201


@app.route("/sell", methods=["POST"])
@error_handle
def post_sell():
    json_data = request.get_json(force=True)

    user = global_store["user"]
    res = user.sell(**json_data)

    return jsonify(res), 201
@app.route("/market_buy", methods=["POST"])
@error_handle
def post_market_buy():
    json_data = request.get_json(force=True)
    user = global_store["user"]
    res = user.market_buy(**json_data)

    return jsonify(res), 201


@app.route("/market_sell", methods=["POST"])
@error_handle
def post_market_sell():
    json_data = request.get_json(force=True)

    user = global_store["user"]
    res = user.market_sell(**json_data)

    return jsonify(res), 201

@app.route("/cancel_entrust", methods=["POST"])
@error_handle
def post_cancel_entrust():
    json_data = request.get_json(force=True)

    user = global_store["user"]
    res = user.cancel_entrust(**json_data)

    return jsonify(res), 201


@app.route("/exit", methods=["GET"])
@error_handle
def get_exit():
    user = global_store["user"]
    user.exit()

    return jsonify({"msg": "exit success"}), 200


def run(port=1430):
    app.run(host="0.0.0.0", port=port)
