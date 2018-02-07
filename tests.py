import requests
import urllib
import time
import hashlib
import hmac
from collections import OrderedDict

server = "https://api.livecoin.net"
api_key = ""
secret_key = ""



def go_get(method, **kwargs):
    data = OrderedDict(sorted((kwargs.items())))
    encoded_data = urllib.parse.urlencode(data)
    sign = hmac.new( secret_key.encode(), msg=encoded_data.encode(), digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign}
    return requests.get(server + method + '?' + encoded_data, headers=headers).json()

def go_post(method, **kwargs):
    data = OrderedDict(sorted((kwargs.items())))
    encoded_data = urllib.parse.urlencode(data)
    sign = hmac.new( secret_key.encode(), msg=encoded_data.encode(), digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign, "Content-type": "application/x-www-form-urlencoded"}
    return requests.post(server + method, encoded_data, headers=headers).json()

#######################################################################################################################
# Функция продажи криптовалюты
def sell(pair,price,quantity):
    sell_stop = True
    i=0
    while i <= 2 and sell_stop:
        sell = go_post('/exchange/selllimit', currencyPair=pair, price=price, quantity=quantity)
        i+=1
        if sell['success']:
            sell_stop = False
            return sell['orderId']
        else:
            print(sell['exception'])

# Функция покупки криптовалюты:
def bids(pair,price,quantity):
    bids_stop = True
    i = 0
    while i <= 2 and bids_stop:
        bids = go_post('/exchange/buylimit', currencyPair=pair, price=price, quantity=quantity)
        i += 1
        if bids['success']:
            bids_stop = False
            return bids['orderId']
        else:
            print(bids['exception'])

#######################################################################################################################

# Функция запроса моих ордеров
def client_orders(pair,openClosed):
    client_orders = go_get('/exchange/client_orders', currencyPair=pair, openClosed=openClosed)
    return client_orders

# Функция закрытия ордера:
def cancellimit(pair,orderId):
    cancellimit = go_post('/exchange/cancellimit', currencyPair=pair, orderId=orderId)
    return cancellimit



#######################################################################################################################

f = open('balans.txt', 'a')

total_USD = go_get('/payment/balances', currency='USD')
print('total_USD', total_USD)
for bal in total_USD:
    print(bal['value'])
    f.write(str(bal) + '\n')
    f.write('========================' + '\n')
#orderId = sell('BTC/USD',80000,0.000100)
currencyP = go_get('/exchange/ticker', currencyPair='BTC/USD')
print('минимальный аск за последние 24 часа',currencyP['min_ask'])
print('максимальный бид за последние 24 часа', currencyP['max_bid'])
print('лучший текущий ASK (Покупка)', currencyP['best_ask'])
print('лучший текущий BID (Продажа)', currencyP['best_bid'])

print('Последняя цена продажи', currencyP['last'])
print('Самая низкая цена продажи', currencyP['low'])




print(currencyP.items())
for cur in currencyP.items():
    print(cur)
print('==================================================================')

last_trades = go_get('/exchange/last_trades', currencyPair='BTC/USD',minutesOrHour='false')
#print(len(last_trades))
list_buy = []
list_sell = []
i = 0
c = 0
for l_t in last_trades:
    #print(l_t.items())
    if l_t['type'] == 'BUY':
        i += 1
        list_buy.append(int(round(float(l_t['price']))))

    if l_t['type'] == 'SELL':
        c += 1
        list_sell.append(int(round(float(l_t['price']))))
mid_BUY_24 = sum(list_buy)/i
mid_SELL_24 = sum(list_sell)/c

#################################################################

veracity_50 = 30
list_buy_10 = []
list_sell_10 = []
j = 0
k = 0
for j_k in last_trades:
    #print(l_t.items())
    if j < veracity_50 and j_k['type'] == 'BUY':
        j += 1
        list_buy_10.append(int(round(float(j_k['price']))))

    if k < veracity_50 and j_k['type'] == 'SELL':
        k += 1
        list_sell_10.append(int(round(float(j_k['price']))))
mid_BUY_50 = sum(list_buy_10)/j
mid_SELL_50 = sum(list_sell_10)/k
#####################################################################


# print('Сортированный BUY',sorted(list_buy))
# print('СОртированный SELL',sorted(list_sell))

print('Средний BUY_24 ==>',mid_BUY_24)
print('Средний SELL_24 ==>',mid_SELL_24)
print(sum(list_sell) / len(list_sell))

print('mid_BUY_50 ==>',mid_BUY_50)
print('mid_SELL_50 ==>',mid_SELL_50)

if mid_BUY_24 < mid_BUY_50:
    print('UP BUY')
    print(mid_BUY_50 - mid_BUY_24)
else:
    print('DOWN BUY')

if mid_SELL_24 < mid_SELL_50:
    print('UP SELL')
    print(mid_SELL_50 - mid_SELL_24)
else:
    print('DOWN SELL')
