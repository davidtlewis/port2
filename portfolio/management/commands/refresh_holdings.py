from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Holding, Transaction

class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):

        for h in Holding.objects.all():
            self.stdout.write(self.style.SUCCESS('about to do holdings' + h.name))
             h.refresh_value()
            