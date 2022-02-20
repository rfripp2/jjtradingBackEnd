import requests
import yfinance as yf
import json
from datetime import datetime
from pprint import pprint

coins_exceptions = ["ceth", "bttold", "icp",
                    "heart", "usdc", "usdt", "mim", "cdai", "ust", "busd", "tusd"]


def getSymbols(ammount_of_coins):
    symbols_array = []
    response = requests.get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={ammount_of_coins}&page=1&sparkline=false")

    for coin in response.json():
        if coin['symbol'] not in coins_exceptions:
            symbols_array.append(coin['symbol'])
    return symbols_array


def symbols_usd(symbols_arr):
    symbols = []
    for symbol in symbols_arr:
        symbols.append(symbol + "-USD")
    return symbols


def get_min_price(pair, period):

    ticker = yf.Ticker(pair)
    df = ticker.history(period=period)
    min_price_date = {
        "pair": pair,
        "min": df['Close'][0],
        "date": None,
        "timestamp": 0
    }

    for i, row in df.iterrows():
        if row['Close'] < min_price_date['min']:
            min_price_date['min'] = row['Close']
            min_price_date['timestamp'] = datetime.timestamp(i)
            min_price_date['date'] = i

    return min_price_date


def get_max_price(pair, period):
    ticker = yf.Ticker(pair)
    df = ticker.history(period=period)
    max_price_date = {
        "pair": pair,
        "min": df['Close'][0],
        "date": None,
        "timestamp": 0
    }

    for i, row in df.iterrows():
        if row['Close'] > max_price_date['min']:
            max_price_date['min'] = row['Close']
            max_price_date['timestamp'] = datetime.timestamp(i)
            max_price_date['date'] = i

    return max_price_date


def filter_today(array):
    now = datetime.now()
    filtered = []
    timestamp_now = datetime.timestamp(now)
    for coin in array:
        if coin['timestamp'] + 86400 >= timestamp_now:
            filtered.append(coin)
    return filtered


def get_mins_max_list(timeframe, ammount_of_coins):
    result = {
        "mins": [],
        "max": []
    }
    today = {
        "mins": None,
        "max": None
    }
    coins = getSymbols(ammount_of_coins)
    coins_usd = symbols_usd(coins)
    for coin in coins_usd:
        result['mins'].append(get_min_price(coin, timeframe))
        result['max'].append(get_max_price(coin, timeframe))
    today['mins'] = filter_today(result['mins'])
    today['max'] = filter_today(result['max'])
    return today


def get_coins_in_min_max(timeframe, ammount_of_coins):

    result = {
        "min": {
            "coins": [],
            "total": 0
        },
        "max": {
            "coins": [],
            "total": 0
        },
        "coins_tracking": ammount_of_coins
    }

    coins_list_min = get_mins_max_list(timeframe, ammount_of_coins)['mins']
    coins_list_max = get_mins_max_list(timeframe, ammount_of_coins)['max']
    for coin in coins_list_min:
        coin['pair'] = coin['pair'].replace("-USD", "")
        result['min']['coins'].append(coin['pair'])
        result['min']['total'] += 1
    for coin in coins_list_max:
        coin['pair'] = coin['pair'].replace("-USD", "")
        result['max']['coins'].append(coin['pair'])
        result['max']['total'] += 1

    pprint(result)
    return json.dumps(result)
