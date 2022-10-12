from http import cookies
import requests
import time
#BUY Я Покупаю, SELL Я Продаю
def okex_best(asset="USDT", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None, filter_minimum=None, filter_crypto=None, filter_fiat=None, filter_rate=0.85, filter_orders=10):
    if type=="SELL":
        type = "BUY"
    else:
        type ="SELL"
    if pay == ["RosBank"]:
        pay = ["Sberbank"]
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU",
        "app-type": "web",
        "devid": "d91dc7b5-b1ca-42b0-83a4-7962c0fc355b",
        "referer": "https://www.okx.com/ru/p2p-markets/rub/buy-usdt",
        "sec-ch-ua":	'"Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
        "sec-ch-ua-mobile":	"?1",
        "sec-ch-ua-platform":	"Android",
        "sec-fetch-dest":	"empty",
        "sec-fetch-mode":	"cors",
        "sec-fetch-site":	"same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "x-cdn": "https://static.okx.com",
        "x-utc": "4"
    }
    data={
        "quoteCurrency": fiat.lower(),
        "baseCurrency": asset.lower(),
        "side": type.lower(),
        "paymentMethod": pay[0],
        "userType": "all",
        "showTrade": False,
        "showFollow": False,
        "showAlreadyTraded": False,
        "isAbleFilter":  False
    }
    if amount != None:
        data["quoteMinAmountPerOrder"] = amount
    response = requests.get('https://www.okx.com/v3/c2c/tradingOrders/books', params=data, headers=headers)
    text = response.json()
    #print(type(text))
    sellers = text["data"][type.lower()]
    count =0
    for seller in sellers:
        count+=1
        price = seller["price"]
        usdt = seller["availableAmount"]
        if filter_crypto != None:
            if float(usdt) < filter_crypto:
                continue
        minimum = seller["quoteMinAmountPerOrder"]
        if filter_minimum != None:
            if int(round(float(minimum),0)) > filter_minimum:
                continue
        maximum = seller["quoteMaxAmountPerOrder"]
        if filter_fiat !=None:
            if int(round(float(maximum),0)) < filter_fiat:
                continue
        rate = seller["completedRate"]
        if float(rate) < filter_rate:
            continue
        orders = seller["completedOrderQuantity"]
        if int(round(float(orders),0)) < filter_orders:
            continue
        nick = seller["nickName"]
        return {"platform":"okex","nick": nick, "pay":pay[0], "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price}

okex_best(type="SELL")