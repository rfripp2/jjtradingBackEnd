from flask import jsonify
import requests
import yfinance as yf
from datetime import datetime, timedelta
import time
import os
from binance.client import Client


# from binance.futures import Futures as Client_Futures
from binance.spot import Spot


coins_exceptions = [
    "ceth",
    "dot",
    "bttold",
    "wbtc",
    "usdc",
    "usdt",
    "mim",
    "cdai",
    "ust",
    "busd",
    "tusd",
    "dai",
    "xaut",
    "paxg",
    "frax",
    "cusdc",
    "hbtc",
    "usdp",
    "cusdt",
    "renbtc",
    "fei",
    "cvxcrv",
    "steth",
    "lusd",
    "usdn",
    "stx",
    "ape",
    "bluna",
]


# Request al endpoint de coingecko,por pagina max 250, osea que tengo que ajustar la funcion para que si se piden mas de 250, haga otro request a la page=2
# Este endpoint retorna mucha inf de cada moneda,symbol,mc etc
def get_coins_inf_cg(quantity):

    coins = requests.get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={quantity}&page=1&sparkline=false",
        timeout=6,
    )
    page_one = coins.json()

    if int(quantity) > 250:
        coins_missing_to_request = int(quantity) - 250

        second_page = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={coins_missing_to_request}&page=2&sparkline=false",
            timeout=6,
        )
        page_two = second_page.json()
        return {"page_two": page_two, "page_one": page_one}
    else:
        return {"page_two": None, "page_one": page_one}


# Esta funcion retorna solamente los symbols, primero almacena las coin inf invocando a la funcion que hace el request a coingecko


def coins_symbols_cg(quantity):
    symbols = []
    coins_inf = get_coins_inf_cg(quantity)

    # FOR son ciclos que recorren un array (lista), para cada item de la lista, va agegando solamente el symbol a symbols que inicialize vacio aca arriba
    for coin in coins_inf["page_one"]:
        if coin["symbol"] not in coins_exceptions:
            symbols.append(coin["symbol"])
    if coins_inf["page_two"]:
        for coin in coins_inf["page_two"]:
            if coin["symbol"] not in coins_exceptions:
                symbols.append(coin["symbol"])
    return symbols


# Esta funcion ejectuta la funcion de arriba que a su vez ejectuta el request a coingecko


def getSymbols(ammount_of_coins):
    return coins_symbols_cg(ammount_of_coins)


# Con el ciclo FOR, a cada symbol le agrega -USD que es necesario para hacer los request a yahoo


def symbols_usd(symbols_arr):
    symbols = []
    for symbol in symbols_arr:
        symbols.append(symbol + "-USD")
    return symbols


# ticker es informacion que se requestea a yahoo del par
# df = dataframe, es una libreria de python para trabajar la inf comodamente
def is_today_min_high(pair, period):
    ticker = yf.Ticker(pair)
    day_index = period.index("d")
    days = period[0:day_index]
    coin = pair.replace("-usd", "")

    df = ticker.history(period=period)
    print(len(df), period)
    print(df)
    result = {"min": False, "max": False, "error": False}
    # Inicializa min y max como la primera vela

    if not df.empty and ticker.info and len(df) == int(days):
        min = df["Close"][0]
        max = df["Close"][0]
        for i, row in df.iterrows():

            # El ciclo FOR va iterando vela por vela, si la vela atual es menor que min, min pasa a ser la vela actual
            if row["Close"] < min:
                min = row["Close"]
            elif row["Close"] > max:
                max = row["Close"]
        # .iloc[-1] equivale a la ultima vela, entonces si min = ultima vela,quiere decir que la vela actual (hoy),esta en minimos

        if min == df["Close"].iloc[-1]:
            result["min"] = True
        elif max == df["Close"].iloc[-1]:
            result["max"] = True
    else:
        return mins_max_binance(coin, int(days))

    # La funcion retorna un objeto con Min,Max,Error que van a tener valores booleanso (True o False), en el front cuando hago este request a x moneda, si me retorna true,la muestra en la lista de min,max o error
    return result


binance_key = os.environ.get("BINANCE_API_KEY")
binance_secret_key = os.environ.get("BINANCE_SECRET_KEY")


# client_binance = Client(binance_key, binance_secret_key)

# client_futures = Futures(binance_key, binance_secret_key)


url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1MIN&time_start=2016-01-01T00:00:00&time_end=2016-02-01T00:00:00"
headers = {"X-CoinAPI-Key": "72785BE9-0392-4BDA-B115-596C3836840F"}
response = requests.get(url, headers=headers)


def get_initial_date_from_days_back(daysback):
    today = datetime.today().replace(
        hour=21, minute=00, second=00, microsecond=00
    ) - timedelta(days=daysback - 1)
    days_back_date = today.isoformat()
    return days_back_date


def mins_max_binance(coin, daysback):
    print("binance api")

    client = Spot()
    msnow = int(round(time.time() * 1000))
    symbol = coin.upper() + "USDT"
    print("symbol:", symbol)

    start_date = datetime.today().replace(
        hour=21, minute=00, second=00, microsecond=00
    ) - timedelta(days=daysback)

    start_miliseconds = round(datetime.timestamp(start_date))

    response = client.klines(
        startTime=start_miliseconds * 1000, symbol=symbol, interval="1d"
    )

    result = {"min": False, "max": False, "error": False}

    min = response[0][4]
    max = response[0][4]

    for candle in response:
        if candle[4] < min:
            min = candle[4]
        elif candle[4] > max:
            max = candle[4]
    if response[-1][4] == min:
        result["min"] = True
    elif response[-1][4] == max:
        result["max"] = True
    print("RESPONSE", coin, response)
    print(result)
    return result


# mins_max_binance("BTC", 7)
# is_today_min_high("BTC-usd", "2d")
