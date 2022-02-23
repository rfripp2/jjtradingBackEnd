from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import *


app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def index():
    return "Home"


@app.route('/api', methods=['GET'])
@cross_origin()
def api():
    return{
        "tutorial": "Flask React Herokuu"
    }


@app.route('/minsmax', methods=['GET'])
@cross_origin()
def prices():
    days_back = request.args.get('days_back')
    coins_quantity = request.args.get('coins_quantity')
    return get_coins_in_min_max(days_back, coins_quantity)


@app.route('/minsmax/coinsexcluded', methods=['GET'])
@cross_origin()
def coins_excluded():
    return json.dumps(coins_exceptions)


@app.route('/minsmax/addcoin/', methods=['PUT'])
@cross_origin()
def add_coin():
    coin = request.args.get('coin')
    print(coin)
    coins_exceptions.append(coin)
    return json.dumps(coins_exceptions)


if __name__ == '__main__':
    app.run()
