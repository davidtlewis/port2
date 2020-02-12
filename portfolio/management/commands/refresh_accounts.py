from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Account

class Command(BaseCommand):
    help = 'sum holdings to refresh account value'
    def handle(self, *args, **options):

        for ac in Account.objects.all():
            self.stdout.write(self.style.SUCCESS('about to do account' + ac.name))
            ac.refresh_value()