import django_filters
from .models import Transaction, Holding, HistoricPrice, Dividend


class TransactionByAccountFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['account',]


class HoldingByAccountFilter(django_filters.FilterSet):
    class Meta:
        model = Holding
        fields = ['account','stock','account__person']

class HistoricPriceByStockFilter(django_filters.FilterSet):
    class Meta:
        model = HistoricPrice
        fields = ['stock',]

class DividendByStockFilter(django_filters.FilterSet):
    class Meta:
        model = Dividend
        fields = ['stock',]