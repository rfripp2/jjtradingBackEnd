from flask import Flask
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


@app.route('/prices', methods=['GET'])
@cross_origin()
def prices():
    return get_coins_in_min_max("2d", 20)


if __name__ == '__main__':
    app.run()
