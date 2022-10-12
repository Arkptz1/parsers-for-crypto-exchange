from binance_p import binance_best 
import requests
def get_currency(pars="BTCUSDT"):
    s = requests.get(f"https://api.binance.com/api/v3/avgPrice?symbol={pars}")
    print(s.json())
asset = ["USDT", "BTC", "BUSD", "BNB", "ETH", "RUB", "SHIB"]
asset = "USDT"
dic = {"USDT": ["BTC", "BUSD", "BNB", "ETH", "RUB", "SHIB"], "BTC":["USDT", "BUSD", "RUB"]}
currency_rub = {}

pay = ["Tinkoff", "RosBank", "YandexMoney", "QIWI"]
filter_crypto = None
filter_minimum = None
filter_fiat = None
amount = None
filter_rate=0.7
filter_orders=10
check_currency = binance_best(asset=asset, pay=pay,
                    filter_crypto=filter_crypto,
                     filter_minimum=filter_minimum,
                      amount=amount, filter_fiat=filter_fiat,
                       filter_rate=filter_rate, filter_orders=filter_orders)

deposit = 100000#int(input("деп в рублях"))
dep_usdt = 100000/ float(check_currency["price"])
print(dep_usdt)
get_currency()