from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from utils import *


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})
CORS_ALLOW_ORIGIN = "*"
CORS_EXPOSE_HEADERS = "*"
CORS_ALLOW_HEADERS = "content-type"
cors = CORS(app, origins=CORS_ALLOW_ORIGIN, allow_headers=CORS_ALLOW_HEADERS,
            expose_headers=CORS_EXPOSE_HEADERS,   supports_credentials=True)


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
    response = jsonify(get_coins_in_min_max(days_back, coins_quantity))
    # response.headers.add('Access-Control-Allow-Origin',
    # 'https://jjtrading-rfripp2.vercel.app')
    return response


@app.route('/minsmax/coinsexcluded', methods=['GET'])
@cross_origin()
def coins_excluded():
    return json.dumps(coins_exceptions)


@app.route('/minsmax/addcoin/', methods=['PUT'], strict_slashes=False)
@cross_origin(supports_credentials=True)
def add_coin():
    coin = request.args.get('coin')
    coins_exceptions.append(coin)
    response = json.dumps(coins_exceptions)

    return response


if __name__ == '__main__':
    app.run()
