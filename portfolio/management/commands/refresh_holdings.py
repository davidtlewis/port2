from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Holding

class Command(BaseCommand):
    help = 'testing refesh all portfolios with method'
    def handle(self, *args, **options):
        
        
        for h in Holding.objects.all():
            h.refresh_value()
            self.stdout.write(self.style.SUCCESS("Refreshed holding: " + str(h)))
            
