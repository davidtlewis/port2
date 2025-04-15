from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Price as Price, Stock
import requests
from bs4 import BeautifulSoup
import locale
from django.utils import timezone
from django.core.cache import cache


class Command(BaseCommand):
    help = 'testing adding a Price'

    def handle(self, *args, **options):
        stock_list = Stock.objects.filter(active=True)
        total_number = len(stock_list)
        counter = 0

        # Initialize the progress cache
        cache.set('price_refresh_progress', {
            'current': 0,
            'total': total_number,
            'current_stock': '',
            'is_running': True
        }, timeout=3600)  # Cache for 1 hour max

        for s in stock_list:
            counter = counter + 1
            message = '[' + str(counter) + ' of ' + str(total_number) + \
                ']: Scraping  price:  ' + s.nickname
            self.stdout.write(self.style.SUCCESS(message))

            # Update progress in cache
            cache.set('price_refresh_progress', {
                'current': counter,
                'total': total_number,
                'current_stock': s.nickname,
                'is_running': True
            }, timeout=3600)

            s.refresh_value()

        # Mark process as complete
        cache.set('price_refresh_progress', {
            'current': total_number,
            'total': total_number,
            'current_stock': 'Complete',
            'is_running': False
        }, timeout=3600)
