from typing import OrderedDict
import requests
#BUY Я ПРОДАЮ, SELL Я ПОКУПАЮ
def bybit_best(asset="USDT", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None, filter_minimum=None, filter_crypto=None, filter_fiat=None, filter_rate=0.85, filter_orders=10): 
    filter_rate = filter_rate * 100
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US",
        "Content-Length": "73",
        "content-type": "application/x-www-form-urlencoded",
        "guid": "c9def04e-721a-3c03-ded0-0d87f8e50e44",
        "lang":	"en-US",
        "Origin": "https://www.bybit.com",
        "platform":	"PC",
        "referer":	"https://www.bybit.com/",
        "sec-ch-ua":	'"Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
        "sec-ch-ua-mobile":	"?1",
        "sec-ch-ua-platform":	"Android",
        "sec-fetch-dest":	"empty",
        "sec-fetch-mode":	"cors",
        "sec-fetch-site":	"same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    pay2 = pay[0]
    if pay == ["Tinkoff"]:
        pay = 75
    elif pay == ["RosBank"]:
        pay = 185
    if type =="BUY":
        type = 1
    elif type == "SELL":
        type =0 
    data={"tokenId": asset,
        "currencyId": fiat,
        "payment": pay, # тинька 75 rosbank 185
        "side": type,  #buy 1, sell 0
        "size": 30,
        "page": 1,
    }
    if amount != None:
        data["amount"] = amount
    response = requests.post('https://api2.bybit.com/spot/api/otc/item/list', data=data, headers=headers)
    text = response.json()
    sellers = text["result"]["items"]
    count =0
    dct = {}
    for seller in sellers:
        count+=1
        price = seller["price"]
        usdt = seller["lastQuantity"]
        if filter_crypto != None:
            if int(round(float(usdt),0)) < filter_crypto:
                continue
        minimum = seller["minAmount"]
        if filter_minimum != None:
            if int(round(float(minimum),0)) > filter_minimum:
                continue
        maximum = seller["maxAmount"]
        if filter_fiat !=None:
            if int(round(float(maximum),0)) < filter_fiat:
                continue
        #time = seller["payTimeLimit"]
        rate = seller["recentExecuteRate"]
        if int(round(float(rate),0)) < filter_rate:
            continue
        orders = seller["recentOrderNum"]
        if int(round(float(orders),0)) < filter_orders:
            continue
        nick = seller["nickName"]
        #print(f"Продавец №{count}\nНик: {nick}\n Рейтинг: {rate}\n кол-во сделок: {orders}\n минималка: {minimum} {fiat}\n максималка: {maximum} {fiat}\nКрипта: {usdt} {asset}\n Цена: {price}\n\n\n")
        return {"platform":"bybit","nick": nick, "pay":pay2, "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price}