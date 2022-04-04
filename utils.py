
from flask import jsonify
import requests
import yfinance as yf
from datetime import datetime
import os
from binance.client import Client
#from binance.futures import Futures as Client_Futures


coins_exceptions = ["ceth", "dot", "bttold", "wbtc",
                    "usdc", "usdt", "mim", "cdai", "ust", "busd", "tusd", "dai", "xaut", "paxg", "frax", "cusdc", "hbtc", "usdp", "cusdt", "renbtc", "fei", "cvxcrv", "steth", "lusd", "usdn", "stx", "ape"]


# Request al endpoint de coingecko,por pagina max 250, osea que tengo que ajustar la funcion para que si se piden mas de 250, haga otro request a la page=2
# Este endpoint retorna mucha inf de cada moneda,symbol,mc etc
def get_coins_inf_cg(quantity):
    coins = requests.get(
        f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={quantity}&page=1&sparkline=false', timeout=6)

    return coins.json()

# Esta funcion retorna solamente los symbols, primero almacena las coin inf invocando a la funcion que hace el request a coingecko


def coins_symbols_cg(quantity):
    symbols = []
    coins_inf = get_coins_inf_cg(quantity)
    # FOR son ciclos que recorren un array (lista), para cada item de la lista, va agegando solamente el symbol a symbols que inicialize vacio aca arriba
    for coin in coins_inf:
        if coin['symbol'] not in coins_exceptions:
            symbols.append(coin['symbol'])
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
    print("dayss", days)

    df = ticker.history(period=period)
    result = {
        "min": False,
        "max": False,
        "error": False
    }
    # Inicializa min y max como la primera vela
    min = df['Close'][0]
    max = df['Close'][0]
    print(len(df), days)
    if not df.empty and ticker.info and len(df) == int(days):
        for i, row in df.iterrows():

            # El ciclo FOR va iterando vela por vela, si la vela atual es menor que min, min pasa a ser la vela actual
            if row['Close'] < min:
                min = row['Close']
            elif row['Close'] > max:
                max = row['Close']
        # .iloc[-1] equivale a la ultima vela, entonces si min = ultima vela,quiere decir que la vela actual (hoy),esta en minimos
        print("max", max)
        print("min:", min)
        print("last:", df['Close'].iloc[-1])
        if min == df['Close'].iloc[-1]:
            result['min'] = True
        elif max == df['Close'].iloc[-1]:
            result['max'] = True
    else:
        result['error'] = True
    print("result", result)
    # La funcion retorna un objeto con Min,Max,Error que van a tener valores booleanso (True o False), en el front cuando hago este request a x moneda, si me retorna true,la muestra en la lista de min,max o error
    return result


# Estas funciones las importo en otro archivo que es nuestra API (con la que nos comunicamos desde el front),por ej en la web,hacemos un request a jjtradingapi/api/minsMax, nuestra api en ese endpoint retorna la funcion is_today_min_max(), asi como goingecko retorna X cuando hacemos el request a su endpoint.
# client_dydx = Client(host='https://api.dydx.exchange')


def get_funding_rate():
    url = 'https://open-api.coinglass.com/api/pro/v1/futures/funding_rates_chart?symbol=BTC&type=U'
    headers = {
        'coinglassSecret': 'dc9b936244504e75a9582dcc7c728908'
    }
    response = requests.request('GET', url, headers=headers)
    response = response.json()
    return response


binance_key = os.environ.get('BINANCE_API_KEY')
binance_secret_key = os.environ.get('BINANCE_SECRET_KEY')


# client_binance = Client(binance_key, binance_secret_key)

# client_futures = Futures(binance_key, binance_secret_key)


def funding_rate_binance():
    futures_client = Client_Futures()
    return futures_client.funding_rate("BTCUSDT", **{'limit': 1000})


def historical_price_binance(interval):
    spot_client = Client(binance_key, binance_secret_key)
    data = spot_client.get_klines(
        symbol="BTCUSDT", interval=interval, limit=1000)

    return data


is_today_min_high("sol-usd", "10d")
