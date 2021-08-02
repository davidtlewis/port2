from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Holding 

class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):

        for h in Holding.objects.all():
            self.stdout.write(self.style.SUCCESS('Refreshing value for holdings: ' + h.stock.name + " / " + h.account.name))
            h.refresh_value()
            