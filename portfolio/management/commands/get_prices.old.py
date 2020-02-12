from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Price as Price, Stock
import requests
from bs4 import BeautifulSoup
import locale
from django.utils import timezone

baseurl1 = "https://markets.ft.com/data/"
baseurl2 = {
    "etfs":"etfs/tearsheet/performance?s=",
    "fund":"funds/tearsheet/performance?s=",
    "equity":"equities/tearsheet/summary?s="
}

class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
        
        for s in Stock.objects.all():
            #self.stdout.write(self.style.SUCCESS('about to do stock' + s.name))
            url = baseurl1 + baseurl2[s.stock_type] + s.code
            #self.stdout.write(self.style.SUCCESS('url: ' + url))
            page = requests.get(url)
            contents = page.content
            soup = BeautifulSoup(contents, 'html.parser')
            scrapped_current_price = soup.find_all("span",class_='mod-ui-data-list__value')[0].string
            current_price = locale.atof(scrapped_current_price)
            if (s.currency == 'gbx'): current_price = current_price / 100
            self.stdout.write(self.style.SUCCESS("Processed: " + s.name + " Price: "+  str(current_price)))
            p = Price(stock = s, price= current_price)
            p.save()
            s.current_price = current_price
            s.price_updated = timezone.now()
            #self.stdout.write(self.style.SUCCESS("s.current_price: " + str(s.current_price) + " time: "+  str(s.price_updated)))
            s.save()
        
