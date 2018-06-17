import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pandas as pd
from datetime import datetime
import tzlocal

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

def find_year(url):
    #Opening up the URL
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
    else:
        return(url)

def find_date(url):
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
            date = date + " 0" + first_half
            return(date)
        else:
            first_half = date[0] + date[1]
            date = date[3:6]
            date = date + " " + first_half
            return(date)
    else:
        return(url)

def find_unix(url):
    # finds maximum price of a coin
    if(url != "N/A"):
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
    else:
        return(url)

def year_day_maxDates(year_day_or_max):
    with open("coins.txt", "r") as f:
        data = json.load(f)
        coin_names = [d["name"] for d in data]
        coin_slug = [d["slug"] for d in data]
    ico_names = ICO_drops("names")

    if (year_day_or_max == "year"):
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
        return(years)
            
    elif (year_day_or_max == "day"):
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
        return(days)

    elif (year_day_or_max == "max"):
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
                url = "https://coinmarketcap.com/currencies/" + item + "/"
                urls.append(url)
            else:
                urls.append("N/A")

        if __name__ == '__main__':
            with Pool(50) as p:
                max_times = p.map(find_unix, urls)
        return(max_times)
            
    else:
        print("invalid")

def calculating_init_date():
    years = year_day_maxDates("year")
    days = year_day_maxDates("day")
    
    dates = []
    for i in range(0,len(days)):
        if (days[i] != "N/A"):
            date = days[i] + ", " + years[i]
            dates.append(date)
        else:
            dates.append("N/A")
    return(dates)

def calculating_max_date():
    max_unixes = year_day_maxDates("max")

    dates = []
    for i in range(0,len(max_unixes)):
        if (max_unixes[i] != "N/A"):
            unix_timestamp = float(max_unixes[i])/1000.0
            local_timezone = tzlocal.get_localzone()
            local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)

            month = local_time.strftime("%B")
            date = local_time.strftime("%d")
            if (len(date) == 1):
                date = "0" + date
            dates.append(local_time.strftime(month[0:3] + " " + date + ", %Y"))
        else:
            dates.append("N/A")
    return(dates)

def initial_price(file):
    df = pd.read_csv(file)
    dates = calculating_init_date()
    
    initial_p = []
    for i in range(0, len(dates)-1):
        if(dates[i] != "N/A"):
            if(dates[i] in df.Date.values):
                price = df[df["Date"] == dates[i]]["Price"].values[0]
                initial_p.append(str("{0:0.2f}".format(int(price * 100)/100.0)))
            else:
                date = dates[i]
                num = int(date[len(date)-1])
                num -= 1
                date = date[:-1] + str(num)
                price = (df[df["Date"] == date]["Price"].values[0])
                initial_p.append(str("{0:0.2f}".format(int(price * 100)/100.0)))
        else:
            initial_p.append(dates[i])

    return(initial_p)

print(calculating_max_date())

'''btc_init = initial_price("btc.txt")
print(btc_init)
eth_init = initial_price("eth.txt")'''



