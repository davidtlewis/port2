from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Price as Price, Stock
import requests
from bs4 import BeautifulSoup
import locale
from django.utils import timezone


class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):
                
        for s in Stock.objects.all():
            self.stdout.write(self.style.SUCCESS('about to do get price for ' + s.nickname))
            s.refresh_value()
        
