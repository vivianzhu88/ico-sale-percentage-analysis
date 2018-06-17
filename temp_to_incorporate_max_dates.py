import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pandas as pd


def find_max (url):
    # finds maximum price of a coin
    r = requests.get(url)
    cont = r.json()
    
    prices = list(map(lambda x: x[1], cont["price_usd"]))
    if prices:
        maxPrice = max(prices)
        return (maxPrice)
    else:
        return (0)

def find_max_unix(url):
    # finds maximum price of a coin
    r = requests.get(url)
    cont = r.json()
    
    prices = list(map(lambda x: x[1], cont["price_usd"]))
    if prices:
        maxPrice = max(prices)
        max_index = prices.index(maxPrice)
        max_unix = cont["price_usd"][max_index][0]
        return (max_unix)
    else:
        return (0)

def maxes():
    # makes a list of all of the maximum prices from CMC
    with open("coins.txt", "r") as f:
        data = json.load(f)
        coin_slug = [d["slug"] for d in data]
        
    urls = []
    for item in coin_slug:
        url = "https://graphs2.coinmarketcap.com/currencies/"+item+"/"
        urls.append(url)

    if __name__ == '__main__':
        with Pool(100) as p:
            max = p.map(find_max, urls)
    return (max)

def max_dates():
    with open("coins.txt", "r") as f:
        data = json.load(f)
        coin_slug = [d["slug"] for d in data]
    
    slugs = []
        for i in range(0,len(coin_names)):
            for z in range(0,len(ico_names)):
                if (coin_names[i] == ico_names[z]):
                    slugs.append(coin_slug[i])
                if (len(slugs)-1 != i):
                    slugs.append("N/A")

#m , u = maxes()
m,u = find_max("https://graphs2.coinmarketcap.com/currencies/bitcoin/")
print(m)
