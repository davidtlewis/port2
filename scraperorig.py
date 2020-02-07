import requests
import csv
from bs4 import BeautifulSoup

baseurl1 = "https://markets.ft.com/data/"
baseurl2 = {
    "etfs":"/tearsheet/performance?s=",
    "funds":"/tearsheet/performance?s=",
    "equities":"/tearsheet/summary?s="
}

with open('stocklist.csv',newline='') as stocklistfile:
    stocklist = csv.DictReader(stocklistfile)
    year1_performance = 0
    year1_sector_performance = 0
    current_price = 0

    with open('scrape_results.csv', 'w', newline='') as results_file:
        stock_results = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
        stock_results.writerow(['stockCode','currentPrice','year1Performance','sector','year1_sector_performance'])
        for stockcode in stocklist:
            url = baseurl1 + stockcode['type'] + baseurl2[stockcode['type']] + stockcode['code']
            print("++++++++++++++++++")
            print(stockcode['code'])
            print(stockcode['type'])
            print(url)
            page = requests.get(url)
            contents = page.content
            soup = BeautifulSoup(contents, 'html.parser')
            current_price = soup.find_all("span",class_='mod-ui-data-list__value')[0].string
            #year1_performance = soup.find("span",string='1 Year change').next_sibling.string
            #year1_performance = soup.find("span",string='1 Year change').next_sibling.find()
            if stockcode['type'] == 'equities':
                year1_performance = soup.find("span",string='1 Year change').next_sibling.get_text()
                sector = '---'
                year1_sector_performance =''
            else:
                year1_performance = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.find_all('td')[3].string
                sector = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.next_sibling.find_all('td')[0].string
                year1_sector_performance = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.next_sibling.find_all('td')[3].string
            print(current_price)
            print(year1_performance)
            print(sector)
            print(year1_sector_performance)
            stock_results.writerow([stockcode['code'],current_price, year1_performance,sector,year1_sector_performance])