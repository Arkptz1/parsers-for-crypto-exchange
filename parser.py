from binance_p import binance_best
from huobi import huobi_best
from okex import okex_best
from bybit import bybit_best
from bitzlato import bitzlato_best
import threading
asset = "USDT"
pay = [["Tinkoff"], ["RosBank"]]
filter_crypto = 100
filter_minimum = None
filter_fiat = None
amount = None
filter_rate=0.7
filter_orders=10
BUY = []
SELL = []
def dops(i,pays):
    BUY.append(i(asset=asset, pay=pays, filter_crypto=filter_crypto, filter_minimum=filter_minimum, amount=amount, filter_fiat=filter_fiat, filter_rate=filter_rate, filter_orders=filter_orders))
    SELL.append(i(type="SELL", asset=asset, pay=pays, filter_crypto=filter_crypto, filter_minimum=filter_minimum, amount=amount, filter_fiat=filter_fiat, filter_rate=filter_rate, filter_orders=filter_orders))
for p in pay:
    pays =p
    for i in [binance_best, okex_best, huobi_best, bybit_best]:
        a = threading.Thread(target=dops, args=[i, pays])
        a.start()
a.join()
        

#print(SELL, "\n\n\n\n", BUY, "\n\n\n\n")
best_price = float(BUY[0]["price"])
best_buy = BUY[0]
for place in BUY:
    price = float(place["price"])
    if price < best_price:
        best_price = float(place["price"])
        best_buy = place

best_price = float(SELL[0]["price"])
best_sell = SELL[0]
for place in SELL:
    price = float(place["price"])
    if price > best_price:
        best_price = float(place["price"])
        best_sell = place

print(best_buy)
print(best_sell)