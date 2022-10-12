from http import cookies
import requests
import time
#BUY Я ПРОДАЮ, SELL Я ПОКУПАЮ
def bitzlato_best(asset="USDT", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None, filter_minimum=None, filter_crypto=None, filter_fiat=None, filter_rate=0.85, filter_orders=10):
    pay2 = pay[0]
    if pay == ["Tinkoff"]:
        pay = 443
    elif pay == ["Rosbank"]:
        pay = 3547
    if type == "BUY":
        type = "purchase"
    elif type == "SELL":
        type = "selling"
    data={"skip": 0,
        "limit": 15,
        "cryptocurrency": asset,
        "currency": fiat,
        "type": type,
        "paymethod": pay,
        "isOwnerVerificated": True,
        "isOwnerTrusted": False,
        "isOwnerActive": True,
        "lang": "en",
    }
    if amount != None:
        data["amount"] = amount
    response = requests.get('https://bitzlato.com/api2/p2p/public/exchange/dsa/', params=data)
    text = response.json()
    #print(type(text))
    sellers = text["data"]
    count =0
    for seller in sellers:
        count+=1
        price = seller["rate"]
        usdt = seller["limitCryptocurrency"]["max"]
        if filter_crypto != None:
            if int(round(float(usdt),0)) < filter_crypto:
                continue
        minimum = seller["limitCurrency"]["min"]
        if filter_minimum != None:
            if int(round(float(minimum),0)) > filter_minimum:
                continue
        maximum = seller["limitCurrency"]["max"]
        if filter_fiat !=None:
            if int(round(float(maximum),0)) < filter_fiat:
                continue
        nick = seller["owner"]
        response2 = requests.get(f'https://bitzlato.com/api2/p2p/public/userinfo/{nick}')
        txt = response2.json()
        #print(txt)
        successDeals = int(txt['dealStats'][-1]['successDeals'])
        orders = int(txt['dealStats'][-1]['totalCount'])
        if int(round(float(orders),0)) < filter_orders:
            continue
        rate  = successDeals/orders
        if float(rate) < filter_rate:
            continue
        #print(f"Продавец №{count}\nНик: {nick}\n минималка: {minimum} {fiat}\n максималка: {maximum} {fiat}\nКрипта: {usdt} {asset}\n Цена: {price}\n\n\n")
        #print({"platform": "bitzlato", "nick": nick, "pay":pay2, "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price})
        return {"platform": "bitzlato", "nick": nick, "pay":pay2, "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price}
