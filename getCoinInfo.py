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

def ICO_drops(names_or_prices):
# retrieves all of the coin names or prices from ICO drops
    page = requests.get("https://icodrops.com/ico-stats/")
    soup = BeautifulSoup(page.content, 'html.parser')
    coin_info = soup.find(class_= "category-desk justify-content-center")
    coin_info2 = coin_info.find_all(class_= "col-md-12 col-12 a_ico")
    
    if (names_or_prices == "prices"):
        prices = []
        for i in range(0,len(coin_info2)):
            coin = coin_info2[i]
            ico_info = coin.find(class_= "token_pr")
            ico_tags = ico_info.find_all("div")
            ico_p = ico_tags[1].get_text()
            ico_p = ico_p.replace("$","")
            prices.append(ico_p)
        prices = list(map(float, prices))
        return(prices)
    elif (names_or_prices == "names"):
        names = []
        for i in range(0,len(coin_info2)):
            coin = coin_info2[i]
            ico_info = coin.find(class_= "ico-main-info")
            ico_a = ico_info.find("a").get_text()
            names.append(ico_a)
        return (names)
    else:
        print("invalid")

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

def calculating_ROI(list):
# calculates ROIs from an input list; the first element is the initial price and the second element is the max price
    if (list[0] == 0 or list[0] == "N/A"):
        return ("N/A")
    else:
        temp = list[1]-list[0]
        temp = (temp/list[0])*100
        return (str("{0:0.2f}".format(int(temp * 100)/100.0)) + "%")

def putting_together():
# puts together the coin name, ICO price, max price, ROI into a txt file
    with open("coins.txt", "r") as f:
        data = json.load(f)
        coin_names = [d["name"] for d in data]
    ico_names = ICO_drops("names")
    ico_prices = ICO_drops("prices")
    coin_max = maxes()

    beg_price = []
    for i in range(0,len(coin_names)):
        for z in range(0,len(ico_names)):
            if (coin_names[i] == ico_names[z]):
                beg_price.append(ico_prices[z])
        if (len(beg_price)-1 != i):
            beg_price.append(0)

    begin_end = []
    for i in range(0,len(beg_price)):
        list1 = [beg_price[i], coin_max[i]]
        begin_end.append(list1)

    if __name__ == '__main__':
        with Pool(100) as p:
            usd_roi = p.map(calculating_ROI, begin_end)

    make_file = pd.DataFrame({
        'Name': coin_names,
        'ICO': beg_price,
        'Max': coin_max,
        'USD_ROI': usd_roi,
    })

    make_file = make_file[['Name', 'ICO', 'Max', 'USD_ROI']]
    make_file.to_csv('coins_info.txt', index=False, encoding='utf-8')

putting_together()

