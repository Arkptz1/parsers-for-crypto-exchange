from cgitb import reset
from http import cookies
import requests
import time
from bs4 import BeautifulSoup
from lxml import html
#BUY Я ПРОДАЮ, SELL Я ПОКУПАЮ
def localbitcoins(asset="BTC", fiat="RUB", pay=["Tinkoff"], tYpe="BUY", amount=None):
    data={"action": tYpe.lower(),
        "currency": fiat,
        "country_code": "RU",
        "online_provider": pay[0].upper(),
        "find-offers": "Поиск",
    }
    if amount != None:
        data["amount"] = amount

    print(data)
    response = requests.get('https://localbitcoins.net/instant-bitcoins/', params=data)
    soup = BeautifulSoup(response.text, features="lxml")
    obmen_list = soup.find_all('tr', {'class': 'clickable'})
    print(type(obmen_list))
    for item in obmen_list:
        user = item.find("td", {'class':'column-user'}).find('a').text
        price = float(item.find("td", {'class':'column-price'}).text.replace(" ", "").replace("\n", "").replace(",", "")[:-3])
        limits = item.find("td", {'class':'column-limit'}).text.replace(" ", "").replace("\n", "").replace(",", "")[:-3].split('-')
        min = int(limits[0])
        max = int(limits[1])
        print(f'{user}\n{price}\n{min}\n{max}\n\n')
localbitcoins()