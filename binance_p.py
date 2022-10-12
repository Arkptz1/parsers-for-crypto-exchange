import requests
#BUY Я ПРОДАЮ, SELL Я ПОКУПАЮ
#"RaiffeisenBankRussia"
#YandexMoney
def binance_best(asset="BTC", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None, filter_minimum=None, filter_crypto=None, filter_fiat=None, filter_rate=0.85, filter_orders=10):
    data={"asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": pay,
        "publisherType": None,
        "rows": 10,
        "tradeType": type,
    #    "transAmount":  "5000"
    }
    if amount != None:
        data["transAmount"] = amount
    response = requests.post('https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=data)
    text = response.json()
    #print(type(text))
    sellers = text["data"]
    count =0
    for seller in sellers:
        count+=1
        price = seller["adv"]["price"]
        usdt = seller["adv"]["tradableQuantity"]
        if filter_crypto != None:
            if float(usdt) < filter_crypto:
                continue
        minimum = seller["adv"]["minSingleTransAmount"]
        if filter_minimum != None:
            if int(round(float(minimum),0)) > filter_minimum:
                continue
        maximum = seller["adv"]["dynamicMaxSingleTransAmount"]
        if filter_fiat !=None:
            if int(round(float(maximum),0)) < filter_fiat:
                continue
        time = seller["adv"]["payTimeLimit"]
        rate = seller["advertiser"]["monthFinishRate"]
        if float(rate) < filter_rate:
            continue
        orders = seller["advertiser"]['monthOrderCount']
        if int(round(float(orders),0)) < filter_orders:
            continue
        nick = seller["advertiser"]["nickName"]
        #print(f"Продавец №{count}\nНик: {nick}\n Рейтинг: {rate}\n кол-во сделок: {orders}\n минималка: {minimum} {fiat}\n максималка: {maximum} {fiat}\nКрипта: {usdt} {asset}\n Время обработки: {time}\n Цена: {price}\n\n\n")
        return {"platform":"binance", "nick": nick, "pay":pay[0], "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price}