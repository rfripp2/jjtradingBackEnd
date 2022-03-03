from flask import jsonify
import requests
import yfinance as yf
import json
from datetime import datetime


start = datetime.now()

coins_exceptions = ["ceth", "dot", "bttold", "wbtc",
                    "usdc", "usdt", "mim", "cdai", "ust", "busd", "tusd", "dai", "xaut", "paxg", "frax", "cusdc", "hbtc", "usdp", "cusdt", "renbtc", "fei", "cvxcrv", "steth", "lusd", "usdn"]


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
        "max": False,
        "error": False
    }

    min = df['Close'][0]
    max = df['Close'][0]

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
    else:
        result['error'] = True
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


is_today_min_high("bnb-usd", "2d")
