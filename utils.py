import requests
import yfinance as yf
import json
from datetime import datetime


start = datetime.now()

coins_exceptions = ["ceth", "bttold",
                    "usdc", "usdt", "mim", "cdai", "ust", "busd", "tusd", "comp", "syn", "dai", "xaut", "paxg", "frax", "cusdc", "hbtc", "usdp", "cusdt", "renbtc", "fei", "cvxcrv", "steth", "lusd", "usdn"]


def get_coins_inf_cg(quantity):
    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={quantity}&page=1&sparkline=false')
    return coins.json()


def coins_symbols_cg(quantity):
    symbols = []
    coins_inf = get_coins_inf_cg(quantity)
    for coin in coins_inf:
        if coin['symbol'] not in coins_exceptions:
            symbols.append(coin['symbol'])
    return symbols


def getSymbols(ammount_of_coins):
    return coins_symbols_cg(ammount_of_coins)


def symbols_usd(symbols_arr):
    symbols = []
    for symbol in symbols_arr:
        symbols.append(symbol + "-USD")
    return symbols


def get_min_max_price(pair, period):
    ticker = yf.Ticker(pair)
    df = ticker.history(period=period)
    min_max_price_date = {
        'min': {
            "pair": pair,
            "min": df['Close'][0],
            "date": None,
            "timestamp": 0
        },
        'max': {
            "pair": pair,
            "max": df['Close'][0],
            "date": None,
            "timestamp": 0
        }
    }
    if not df.empty and ticker.info:
        for i, row in df.iterrows():
            if row['Close'] < min_max_price_date['min']['min']:
                min_max_price_date['min']['min'] = row['Close']
                min_max_price_date['min']['timestamp'] = datetime.timestamp(
                    i)
                min_max_price_date['min']['date'] = i
            elif row['Close'] > min_max_price_date['max']['max']:
                min_max_price_date['max']['max'] = row['Close']
                min_max_price_date['max']['timestamp'] = datetime.timestamp(
                    i)
                min_max_price_date['max']['date'] = i

    return min_max_price_date


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
        "max": [],
    }
    today = {
        "mins": None,
        "max": None,
        "tracked": 0,
        'errors': []
    }
    coins = getSymbols(ammount_of_coins)
    coins_usd = symbols_usd(coins)
    for coin in coins_usd:
        try:
            minmax = get_min_max_price(coin, timeframe)
            result['mins'].append(minmax['min'])
            result['max'].append(minmax['max'])
            today['tracked'] += 1
        except IndexError:
            today['errors'].append(coin)
            continue
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
        "coins_without_exceptions": ammount_of_coins,
        "coins_tracked_after": None,
        'coins_errors': ["a"]

    }

    mins_max_list = get_mins_max_list(timeframe, ammount_of_coins)
    coins_list_min = mins_max_list['mins']
    coins_list_max = mins_max_list['max']
    result['coins_tracked_after'] = mins_max_list['tracked']
    result['coins_errors'] = mins_max_list['errors']
    for coin in coins_list_min:
        coin['pair'] = coin['pair'].replace("-USD", "")
        result['min']['coins'].append(coin['pair'])
        result['min']['total'] += 1
    for coin in coins_list_max:
        coin['pair'] = coin['pair'].replace("-USD", "")
        result['max']['coins'].append(coin['pair'])
        result['max']['total'] += 1

    print(result)
    return result
