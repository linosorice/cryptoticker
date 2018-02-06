import requests, json, serial, threading, time, locale

def get_global_market_cap():
    r = requests.get("https://api.coinmarketcap.com/v1/global/")
    data = json.loads(r.text)
    return data['total_market_cap_usd']

def get_coin_price(coin):
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/" + coin)
    data = json.loads(r.text)
    return data[0]['price_usd'], data[0]['percent_change_24h']

def get_prices(seconds):
    market_cap = get_global_market_cap()
    serial_print('Tot Market Cap', market_cap, None)
    time.sleep(seconds)
    btc_price, btc_change_24h = get_coin_price('bitcoin')
    serial_print('BTC/USD 24h', btc_price, btc_change_24h)
    time.sleep(seconds)
    eth_price, eth_change_24h = get_coin_price('ethereum')
    serial_print('ETH/USD 24h', eth_price, eth_change_24h)
    time.sleep(seconds)
    nem_price, nem_change_24h = get_coin_price('nem')
    serial_print('XEM/USD 24h', nem_price, nem_change_24h)
    time.sleep(seconds)
    serial_print_one_line_text('HODL')
    time.sleep(seconds)
    get_prices(seconds)

def serial_print(coin, price, change):
    text = locale.format('%.2f', float(price), True)
    if change:
        formatted_change = locale.format('%.2f', float(change), True)
        text += ' ' + formatted_change + '%'
    ser = serial.Serial('/dev/ttyUSB0')
    ser.write('<ID00><PA><L1>%s<L2>%s<E>' % (coin, text))
    ser.close()

def serial_print_one_line_text(text):
    ser = serial.Serial('/dev/ttyUSB0')
    ser.write('<ID01><PA><FQ>%s<E>' % (text))

locale.setlocale(locale.LC_NUMERIC, 'en_GB.utf8')
get_prices(3)
