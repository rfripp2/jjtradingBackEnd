from utils import *
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify

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


@app.route('/api/max_today', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def max_today():
    days_back = request.args.get('days_back')
    pair = request.args.get('pair')
    response = jsonify(is_today_high(pair, days_back))
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


if __name__ == '__main__':
    app.run()
