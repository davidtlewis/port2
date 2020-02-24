from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Holding, Transaction

class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):

        for h in Holding.objects.all():
            h.refresh_value()
            