import requests
import yfinance as yf
import json
from datetime import datetime


start = datetime.now()

coins_exceptions = ["ceth", "dot", "bttold",
                    "usdc", "usdt", "mim", "cdai", "ust", "busd", "tusd", "comp", "syn", "dai", "xaut", "paxg", "frax", "cusdc", "hbtc", "usdp", "cusdt", "renbtc", "fei", "cvxcrv", "steth", "lusd", "usdn"]


def get_coins_inf_cg(quantity):
    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={quantity}&page=1&sparkline=false', timeout=6)
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


def is_today_min_high(pair, period):
    ticker = yf.Ticker(pair)
    df = ticker.history(period=period)
    result = {
        "min": False,
        "max": False
    }
    min = df['Close'][0],
    max = df['Close'][0],

    if not df.empty and ticker.info:
        for i, row in df.iterrows():
            if row['Close'] < min:
                min = row['Close']
            elif row['Close'] > max:
                max = row['Close']
        if min == df['Close'].iloc[-1]:
            result['min'] = True
        elif max == df['Close'].iloc[-1]:
            result['max'] = True
    return result


def is_today_high(pair, period):
    ticker = yf.Ticker(pair)
    df = ticker.history(period=period)
    max = df['Close'][0],

    if not df.empty and ticker.info:
        for i, row in df.iterrows():
            if row['Close'] > min:
                max = row['Close']
        if max == df['Close'].iloc[-1]:
            print("last row", row['Close'])
            return True
        else:
            return False


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
