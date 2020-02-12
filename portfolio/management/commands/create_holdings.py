from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Holding, Transaction

class Command(BaseCommand):
    help = 'testing adding a Price'
    def handle(self, *args, **options):

        for t in Transaction.objects.all():
                    Holding.objects.get_or_create(
                        account=t.account,
                        stock=t.stock,
                        defaults={'book_cost': 0,'volume': 0, 'current_value': 0},
                    )     
                    #self.stdout.write(self.style.SUCCESS("created if necessary  holding: "))
