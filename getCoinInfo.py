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


def ICO_drops_links():
# retrieves the links for all of the coins on ICOdrops
    links = []
    page = requests.get("https://icodrops.com/ico-stats/")
    soup = BeautifulSoup(page.content, 'html.parser')
    coin_info = soup.find(class_= "category-desk justify-content-center")
    coin_info2 = coin_info.find_all(class_= "col-md-12 col-12 a_ico")
    for item in coin_info2:
        a_tag = item.find("a")
        my_href = a_tag.get("href")
        links.append(my_href)
    return(links)

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
    temp = list[1]-list[0]
    if (list[0] == 0):
        return ("N/A")
    else:
        temp = (temp/list[0])*100
        return (str("{0:0.2f}".format(int(temp * 100)/100.0)) + "%")

def find_year(url):
# opening up the URL for CMC and finding the initial release year
    if(url != "N/A"):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        historical_data = soup.find(id = "historical-data")
        table = historical_data.find(class_= "table")
        tbody_table = historical_data.find("tbody")
        all_days = tbody_table.find_all("tr")
        
        first_day = all_days[len(all_days)-1]
        day_info = first_day.find_all('td')
        date = day_info[0].get_text()
        year = date[len(date)-4] + date[len(date)-3] + date[len(date)-2] + date[len(date)-1]
        return(year)
        print(year)
    else:
        return(url)

def find_date(url):
# opening up the URL for ICOdrops and finding the initial release date w/o year
    if(url != "N/A"):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        pt1 = soup.find(class_ = "white-desk ico-desk")
        pt2 = pt1.find(class_= "sale-date").get_text()
        
        space = pt2.index(" ")
        date = pt2
        if (space == 1):
            first_half = date[0]
            date = date[2:5]
            date = date + " " + first_half
            return(date)
        else:
            first_half = date[0] + date[1]
            date = date[3:6]
            date = date + " " + first_half
            return(date)
    else:
        return(url)

def calculating_date():
# takes year info from CMC and date info from ICOdrops to and combines it together
    with open("coins.txt", "r") as f:
        data = json.load(f)
        coin_names = [d["name"] for d in data]
        coin_slug = [d["slug"] for d in data]
    ico_names = ICO_drops("names")

    # generates the urls needed to access the years on CMC
    slugs = []
    for i in range(0,len(coin_names)):
        for z in range(0,len(ico_names)):
            if (coin_names[i] == ico_names[z]):
                slugs.append(coin_slug[i])
            if (len(slugs)-1 != i):
                slugs.append("N/A")

    urls = []
    for item in slugs:
        if(item != "N/A"):
            url = "https://coinmarketcap.com/currencies/" + item + "/historical-data/?start=20130428&end=20180606"
            urls.append(url)
        else:
            urls.append("N/A")

    if __name__ == '__main__':
        with Pool(50) as p:
            years = p.map(find_year, urls)

    # generates the urls needed to access the dates on ICOdrops
    ico_links = ICO_drops_links()
    urls2 = []
    for i in range(0,len(coin_names)):
        for z in range(0,len(ico_names)):
            if (coin_names[i] == ico_names[z]):
                urls2.append(ico_links[z])
            if (len(urls2)-1 != i):
                urls2.append("N/A")

    if __name__ == '__main__':
        with Pool(50) as p:
            days = p.map(find_date, urls2)

    dates = []
    for i in range(0,len(days)):
        if (days[i] != "N/A"):
            date = days[i] + ", " + years[i]
            dates.append(date)
        else:
            dates.append("N/A")

    return(dates)


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
            roi = p.map(calculating_ROI, begin_end)

    dates = calculating_date()

    make_file = pd.DataFrame({
       'Name': coin_names,
       'ICO': beg_price,
       'Max': coin_max,
       'ROI': roi
    })

    make_file = make_file[['Name', 'ICO', 'Max', 'ROI']]
    make_file.to_csv('coins_info.txt', index=False, encoding='utf-8')



