from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command
import threading
from portfolio.models import Stock
from django.core.cache import cache


class RefreshAccountsView(APIView):
    def post(self, request, *args, **kwargs):
        def run_refresh():
            call_command('refresh_accounts')

        thread = threading.Thread(target=run_refresh)
        thread.start()
        return Response({"message": "Refresh started."}, status=status.HTTP_202_ACCEPTED)


class RefreshPricesView(APIView):
    def post(self, request, *args, **kwargs):
        def run_price_refresh():
            call_command('get_prices')

        thread = threading.Thread(target=run_price_refresh)
        thread.start()

        # Get the total number of active stocks for progress context
        total_stocks = Stock.objects.filter(active=True).count()
        return Response({
            "message": "Price refresh started.",
            "total_stocks": total_stocks
        }, status=status.HTTP_202_ACCEPTED)


class PriceRefreshProgressView(APIView):
    """
    API endpoint to check the progress of the price refresh process
    """

    def get(self, request, *args, **kwargs):
        # Get progress data from cache
        progress_data = cache.get('price_refresh_progress', {
            'current': 0,
            'total': 0,
            'current_stock': 'Not started',
            'is_running': False
        })

        return Response(progress_data)
