import requests
#BUY Я Покупаю, SELL Я Продаю
def huobi_best(asset="USDT", fiat="RUB", pay=["Tinkoff"], type="BUY", amount=None, filter_minimum=None, filter_crypto=None, filter_fiat=None, filter_rate=0.85, filter_orders=10):
    filter_rate = filter_rate * 100
    if type=="SELL":
        type = "BUY"
    else:
        type ="SELL"
    if asset == "USDT":
        asset = 2
    elif asset == "BTC":
        asset = 1
    if fiat == "RUB":
        fiat = 11
    pay2 = pay[0]
    if pay == ["Tinkoff"]:
        pay = 28
    elif pay == ["RosBank"]:
        pay = 29
    data={"coinId": asset,
        "currency": fiat,
        "tradeType": type.lower(),
        "currPage": 1,
        "payMethod": pay,
        "acceptOrder": 0,
        "blockType": "general",
        "online": "1",
        "range": 0,
        "onlyTradable":  True
    }
    if amount != None:
        data["amount"] = amount
    response = requests.get('https://otc-api.trygofast.com/v1/data/trade-market', params=data)
    text = response.json()
    #print(type(text))
    sellers = text["data"]
    count =0
    for seller in sellers:
        count+=1
        price = seller["price"]
        usdt = seller["tradeCount"]
        if filter_crypto != None:
            if float(usdt) < filter_crypto:
                continue
        minimum = seller["minTradeLimit"]
        if filter_minimum != None:
            if int(round(float(minimum),0)) > filter_minimum:
                continue
        maximum = seller["maxTradeLimit"]
        if filter_fiat !=None:
            if int(round(float(maximum),0)) < filter_fiat:
                continue
        rate = seller["orderCompleteRate"]
        if float(rate) < filter_rate:
            continue
        orders = seller["tradeMonthTimes"]
        if int(round(float(orders),0)) < filter_orders:
            continue
        nick = seller["userName"]
        #print(f"Продавец №{count}\nНик: {nick}\n Рейтинг: {rate}\n кол-во сделок: {orders}\n минималка: {minimum} {fiat}\n максималка: {maximum} {fiat}\nКрипта: {usdt} {asset}\n Цена: {price}\n\n\n")
        return {"platform":"huobi","nick": nick, "pay":pay2, "crypto":usdt, "min":minimum, "max":maximum, "rate":rate, "orders":orders, "price":price}
