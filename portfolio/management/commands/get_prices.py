from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Price as Price, Stock
import requests
from bs4 import BeautifulSoup
import locale
from django.utils import timezone


class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):
        stock_list = Stock.objects.filter(active=True)
        total_number = len(stock_list)        
        counter = 0
        for s in stock_list:
            counter = counter + 1
            message = '[' +  str(counter) + ' of ' + str(total_number) +']: Scraping  price:  ' + s.nickname
            self.stdout.write(self.style.SUCCESS(message))
            s.refresh_value()
    
