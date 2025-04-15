from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Account


class Command(BaseCommand):
    help = 'Sum holdings to refresh account value and provide progress updates.'

    def handle(self, *args, **options):
        accounts = Account.objects.all()
        total_accounts = accounts.count()

        if total_accounts == 0:
            self.stdout.write(self.style.WARNING(
                'No accounts found to refresh.'))
            return

        for index, ac in enumerate(accounts, start=1):
            self.stdout.write(
                f'Refreshing account {index}/{total_accounts}: {ac.name}')
            ac.refresh_value()
            progress = (index / total_accounts) * 100
            self.stdout.write(self.style.SUCCESS(f'Progress: {progress:.2f}%'))

        self.stdout.write(self.style.SUCCESS(
            'All accounts have been refreshed successfully.'))
