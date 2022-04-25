from utils import *
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask import Flask, request, jsonify, abort, session
import json
from config import ApplicationConfig
from models import db, User, ReportMinsMax


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.secret_key = "secret"
bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)
with app.app_context():
    db.create_all()


cors = CORS(app, supports_credentials=True)


@app.route("/")
@cross_origin()
def index():
    return "Home"


@app.route("/me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthroized"})
    user = User.query.filter_by(id=user_id).first()
    return jsonify({"username": user.username, "id": user_id})


@app.route("/createUser", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]

    user_exists = User.query.filter_by(username=username).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(password=hashed_password, username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "username": new_user.username})


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({"id": user.id, "username": user.username})


@app.route("/createreport", methods=["POST"])
def post_report():
    errors = request.json["errors"]
    days_back = request.json["days_back"]
    coins_requested = request.json["coins_requested"]
    max = request.json["max"]
    min = request.json["min"]
    date = request.json["date"]
    owner_id = session.get("user_id")

    new_report = ReportMinsMax(
        errors=errors,
        days_back=days_back,
        coins_requested=coins_requested,
        max=max,
        min=min,
        owner_id=owner_id,
        date=date,
    )

    db.session.add(new_report)
    db.session.commit()
    return jsonify({"owner_id": new_report.owner_id})


@app.route("/getreport", methods=["GET"])
def get_reports():

    reports = ReportMinsMax.query.filter_by(owner_id=session.get("user_id")).all()
    result = []
    for row in reports:
        result.append(
            {
                "max": row.max,
                "coins_requested": row.coins_requested,
                "date": row.date,
                "min": row.min,
                "max": row.max,
                "days_back": row.days_back,
                "errors": row.errors,
            }
        )
    return jsonify(result)


@app.route("/api/coins/<quantity>", methods=["GET"])
@cross_origin()
def getCoins(quantity):
    coins = jsonify(getSymbols(quantity))
    return coins


@app.route("/api/min_max_today", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
def min_today():
    days_back = request.args.get("days_back")
    pair = request.args.get("pair")
    response = is_today_min_high(pair, days_back)
    print(response)
    return jsonify(response)


@app.route("/api/minsmax/coinsexcluded", methods=["GET"])
@cross_origin()
def coins_excluded():
    return json.dumps(coins_exceptions)


@app.route("/api/minsmax/addcoin/", methods=["PUT"], strict_slashes=False)
@cross_origin()
def add_coin():
    coin = request.args.get("coin")
    coins_exceptions.append(coin)
    response = json.dumps(coins_exceptions)
    return response


@app.route("/api/fundingrate", methods=["GET"])
@cross_origin()
def funding_rate():
    return get_funding_rate()


@app.route("/api/binance_funding", methods=["GET"])
@cross_origin()
def binance_funding():
    return funding_rate_binance()


@app.route("/api/history", methods=["GET"])
@cross_origin()
def history():
    candlesticks = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 March,2022", "9 March,2022"
    )
    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {"x": data[0], "y": [data[1], data[2], data[3], data[4]]}

        processed_candlesticks.append(candlestick)
    return jsonify(processed_candlesticks)


@app.route("/api/fundinghistory", methods=["GET"])
@cross_origin()
def fundinghistory():
    data = funding_rate_binance()
    processed_data = []
    for candle in data:

        new_data = {
            "time": int(candle["fundingTime"] / 1000),
            "value": float(candle["fundingRate"]) * 100 * 3 * 365,
        }
        processed_data.append(new_data)
    return jsonify(processed_data)


@app.route("/api/historicalprice", methods=["GET"])
@cross_origin()
def historical_price():
    interval = request.args.get("interval")
    candlesticks = historical_price_binance(interval)
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4],
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
