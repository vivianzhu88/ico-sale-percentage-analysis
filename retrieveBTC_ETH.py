import requests
from bs4 import BeautifulSoup
import pandas as pd

def currency(url, df):
    #Opening up the URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    historical_data = soup.find(id = "historical-data")
    table = historical_data.find(class_= "table")
    tbody_table = historical_data.find("tbody")
    all_days = tbody_table.find_all("tr")
    
    date = []
    avg_price =[]
    
    for i in range(0, len(all_days)):
        temp = all_days[i]
        day = temp.find_all('td')
        
        date.append(day[0].get_text())
        open_price = float(day[1].get_text())
        close_price = float(day[4].get_text())
        avg = (open_price+close_price)/2
        avg_price.append(str("{0:0.3f}".format(int(avg * 100)/100.0)))
        
    #Putting data into a csv file
    info = pd.DataFrame({
       'Date': date,
       'Price': avg_price,
       })
    info = info[['Date','Price']]
    info.to_csv(df, index=False, encoding='utf-8')


currency("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20180606", "btc.txt")
currency("https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end=20180606", "eth.txt")
