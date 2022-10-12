from http import cookies
import requests
import time
def bitzlato(asset="BTC", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None):
    if pay == ["Tinkoff"]:
        pay = "B3"
    elif pay == ["Rosbank"]:
        pay = 3547
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru",
        "app-type": "web",
        "sec-ch-ua":'"Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
        "sec-ch-ua-mobile":	"?0",
        "sec-ch-ua-platform":	"Windows",
        "sec-fetch-dest":	"empty",
        "sec-fetch-mode":	"cors",
        "sec-fetch-site":	"same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "x-access-token": "",
        "x-device-type": "web"
    }
    data={
        "type": type.lower(),
        "page": 1,
        "sort": "-price",
        "currency_code": fiat,
        "previous_currency_code": fiat,
        "crypto_currency_code": asset,
        "payment_method_bank_code": pay,
        "with_correct_limits": "false",
        "limit": 20,
        "pages": 1,
        "total":10
    }
    if amount != None:
        data["amount"] = amount
    print(data)
    response = requests.get('https://bitpapa.com/api/v1/pro/search', params=data, headers=headers)
    print(response.)
    text = response.json()
    print(text)
    #print(type(text))
    sellers = text["data"]
    count =0
    for seller in sellers:
        count+=1
        price = seller["rate"]
        usdt = seller["limitCryptocurrency"]["max"]
        minimum = seller["limitCurrency"]["min"]
        maximum = seller["limitCurrency"]["max"]
        nick = seller["owner"]
        print(f"Продавец №{count}\nНик: {nick}\n минималка: {minimum} {fiat}\n максималка: {maximum} {fiat}\nКрипта: {usdt} {asset}\n Цена: {price}\n\n\n")
        if count == 10:
            break
    a=input()
    print(sellers)
bitzlato()