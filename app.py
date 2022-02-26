from flask import Flask, request, jsonify
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


@app.route('/api/minsmax', methods=['GET'])
@cross_origin(origin='https://jjtrading-rfripp2.vercel.app', headers=['Content-Type', 'Authorization'])
def prices():
    days_back = request.args.get('days_back')
    coins_quantity = request.args.get('coins_quantity')
    response = jsonify(get_coins_in_min_max(days_back, coins_quantity))
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
