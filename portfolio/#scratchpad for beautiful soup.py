#scratchpad for beautiful snoop 
from bs4 import BeautifulSoup
import locale
import requests
page = requests.get("https://markets.ft.com/data/etfs/tearsheet/performance?s=VUKE:LSE:GBP")
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')

soup.find("div", class_='mod-ui-table--freeze-pane__scroll-container').find_all("tr")
soup.find("div", class_='mod-ui-table--freeze-pane__scroll-container').find_all("tr")[1]
soup.find("div", class_='mod-ui-table--freeze-pane__scroll-container').find_all("tr")[1].find_all("td")[1].string
perf= locale.atof(scrapped_perf[:-1])



from bs4 import BeautifulSoup
import locale
import requests
page = requests.get("https://finance.yahoo.com/quote/VWRL.L?p=VWRL.L")
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
soup.find("span", attrs={"data-reactid": "31"})

from bs4 import BeautifulSoup
import locale
from requests_html import HTMLSession
session = HTMLSession() 
page = session.get("https://finance.yahoo.com/quote/VWRL.L?p=VWRL.L")
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
soup.find("span", attrs={"data-reactid": "31"})