import requests, json, serial, threading, time, locale

def get_global_market_cap():
    r = requests.get("https://api.coinmarketcap.com/v1/global/")
    data = json.loads(r.text)
    return data['total_market_cap_usd']

def get_bitcoin_price():
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    data = json.loads(r.text)
    return data[0]['price_usd']

def get_ethereum_price():
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/ethereum/")
    data = json.loads(r.text)
    return data[0]['price_usd']

def get_prices(seconds):
    market_cap = get_global_market_cap()
    print market_cap
    serial_print('Tot Market Cap', market_cap)
    time.sleep(seconds)
    btc_price = get_bitcoin_price()
    print btc_price
    serial_print('BTC/USD', btc_price)
    time.sleep(seconds)
    eth_price = get_ethereum_price()
    print eth_price
    serial_print('ETH/USD', eth_price)
    time.sleep(seconds)
    get_prices(seconds)

def serial_print(coin, price):
    formatted_price = locale.format('%.2f', float(price), True)
    ser = serial.Serial('/dev/ttyUSB0')
    ser.write('<ID00><PA><L1>%s<L2>%s<E>' % (coin, formatted_price))
    ser.close()

locale.setlocale(locale.LC_NUMERIC, 'en_GB.utf8')
get_prices(3)
