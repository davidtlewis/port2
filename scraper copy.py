import requests
from bs4 import BeautifulSoup

baseurl1 = "https://markets.ft.com/data/"
baseurl2 = {
    "etfs":"/tearsheet/performance?s=",
    "funds":"/tearsheet/performance?s=",
    "equities":"/tearsheet/summary?s="
}

url = baseurl1 + stockcode['type'] + baseurl2[stockcode['type']] + stockcode['code']
page = requests.get(url)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
current_price = soup.find_all("span",class_='mod-ui-data-list__value')[0].string
"""
if stockcode['type'] == 'equities':
    year1_performance = soup.find("span",string='1 Year change').next_sibling.get_text()
    sector = '---'
    year1_sector_performance =''
else:
    year1_performance = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.find_all('td')[3].string
    sector = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.next_sibling.find_all('td')[0].string
    year1_sector_performance = soup.find("table",class_='mod-ui-table--freeze-pane').tbody.tr.next_sibling.find_all('td')[3].string
"""
