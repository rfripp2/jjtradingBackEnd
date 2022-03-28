from utils import *
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import json


app = Flask(__name__)
cors = CORS(app)


@app.route('/')
@cross_origin()
def index():
    return "Home"


@app.route('/api', methods=['GET'])
@cross_origin()
def api():
    return{
        "tutorial": "Flask React Herokuuu"
    }


@app.route('/api/coins/<quantity>', methods=['GET'])
@cross_origin()
def getCoins(quantity):
    coins = jsonify(getSymbols(quantity))
    return coins


@app.route('/api/min_max_today', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def min_today():
    days_back = request.args.get('days_back')
    pair = request.args.get('pair')
    response = jsonify(is_today_min_high(pair, days_back))
    print(response)
    return response


@app.route('/api/minsmax/coinsexcluded', methods=['GET'])
@cross_origin()
def coins_excluded():
    return json.dumps(coins_exceptions)


@app.route('/api/minsmax/addcoin/', methods=['PUT'], strict_slashes=False)
@cross_origin()
def add_coin():
    coin = request.args.get('coin')
    coins_exceptions.append(coin)
    response = json.dumps(coins_exceptions)
    return response


@app.route('/api/fundingrate', methods=['GET'])
@cross_origin()
def funding_rate():
    return get_funding_rate()


@app.route('/api/binance_funding', methods=['GET'])
@cross_origin()
def binance_funding():
    return funding_rate_binance()


@app.route('/api/history', methods=['GET'])
@cross_origin()
def history():
    candlesticks = client.get_historical_klines(
        "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "7 March,2022", "9 March,2022")
    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            "x": data[0],
            "y": [data[1], data[2], data[3], data[4]]
        }

        processed_candlesticks.append(candlestick)
    return jsonify(processed_candlesticks)


@app.route('/api/fundinghistory', methods=['GET'])
@cross_origin()
def fundinghistory():
    data = funding_rate_binance()
    processed_data = []
    for candle in data:

        new_data = {
            "time": int(candle['fundingTime'] / 1000),
            "value": float(candle['fundingRate']) * 100 * 3 * 365,
        }
        processed_data.append(new_data)
    return jsonify(processed_data)


@app.route('/api/historicalprice', methods=['GET'])
@cross_origin()
def historical_price():
    interval = request.args.get('interval')
    candlesticks = historical_price_binance(interval)
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


if __name__ == '__main__':
    app.run()
